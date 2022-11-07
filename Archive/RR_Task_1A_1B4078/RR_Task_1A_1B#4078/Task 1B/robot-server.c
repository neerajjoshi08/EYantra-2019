/*
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1B of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
*/

/*
* Team ID:			[ 4078 ]
* Author List:		[ Ashish Chhabra, Mayank Singhal, Neeraj Joshi, Nitin Jayant ]
* Filename:			robot-server.c
* Functions:		socket_create, receive_from_send_to_client
* 					[ format_and_store, parse_obstacles ]
* Global variables:	SERVER_PORT, RX_BUFFER_SIZE, TX_BUFFER_SIZE, MAXCHAR,
* 					dest_addr, source_addr, rx_buffer, tx_buffer,
* 					ipv4_addr_str, ipv4_addr_str_client, listen_sock, line_data, input_fp, output_fp
* 					[ List of global variables defined in this file ]
*/


// Include necessary header files
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <arpa/inet.h>


// Constants defined
#define SERVER_PORT 3333
#define RX_BUFFER_SIZE 1024
#define TX_BUFFER_SIZE 1024

#define MAXCHAR 1000				// max characters to read from txt file

// Global variables
struct sockaddr_in dest_addr;
struct sockaddr_in source_addr;

char rx_buffer[RX_BUFFER_SIZE];		// buffer to store data from client
char tx_buffer[RX_BUFFER_SIZE];		// buffer to store data to be sent to client

char ipv4_addr_str[128];			// buffer to store IPv4 addresses as string
char ipv4_addr_str_client[128];		// buffer to store IPv4 addresses as string

int listen_sock;

char line_data[MAXCHAR];

FILE *input_fp, *output_fp;

/*
* Function Name:	format_and_store
* Inputs:			ptr [ pointer to the string containing obstacles ]
* 					obs [ array on which parsed obstacle is to be stored ]
* Outputs: 			None
* Purpose: 			Parses single obstacle and formats it according to nomenclature
* Example call: 	format_and_store(ptr, obs[maze][obstacle_count++]);
*/
void format_and_store(char *ptr, char *obs){
        int i;
        char *pos;
        obs[0] = '@';
        for (pos=ptr, i=1; *pos!='\0'; pos++){
               if ((*pos == ' ') || (*pos == '\n') || (*pos == '\r')){
                       continue;
               }
               obs[i++] = *pos;
        }

        obs[i] = '@';
}


/*
* Function Name:	parse_obstacles
* Inputs:			obs [ 3D array of all obstacles ]
* Outputs: 			None
* Purpose: 			Parses all the obstacles and formats it using format_and_store
* Example call: 	parse_obstacles(obs);
*/
void parse_obstacles(char (*obs)[3][10]){
    int maze;
    char *ptr;
    int obcount=0;
	int i,j;
    do{
            obcount=0;
            if (strlen(line_data)<4){
                continue;
            }   

            maze = line_data[0] - '0';
            ptr = strtok(&line_data[3], ";");
            while (ptr!=NULL){
                    format_and_store(ptr, obs[maze][obcount++]);
                    ptr = strtok(NULL, ";");
            }
    }while(fgets(line_data, 1000, input_fp)!=NULL);

}   


/*
* Function Name:	socket_create
* Inputs:			dest_addr [ structure type for destination address ]
* 					source_addr [ structure type for source address ]
* Outputs: 			my_sock [ socket value, if connection is properly created ]
* Purpose: 			the function creates the socket connection with the server
* Example call: 	int sock = socket_create(dest_addr, source_addr);
*/
int socket_create(struct sockaddr_in dest_addr, struct sockaddr_in source_addr){

	int addr_family;
	int ip_protocol;

	dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	dest_addr.sin_family = AF_INET;
	dest_addr.sin_port = htons(SERVER_PORT);
	addr_family = AF_INET;
	ip_protocol = IPPROTO_IP;

	int my_sock;

	socklen_t source_size;
	int yes=1;

	listen_sock = socket(addr_family, SOCK_STREAM, ip_protocol);
	

	//Reuse port
	if (setsockopt(listen_sock,SOL_SOCKET,SO_REUSEADDR,&yes,sizeof yes) == -1) {
		perror("setsockopt");
		exit(1);
	} 

	if(bind(listen_sock, (struct sockaddr *)&dest_addr, sizeof dest_addr)==-1){
		printf("\nCouldn't Bind");
		exit(1);
	}

	inet_ntop(addr_family, &(dest_addr.sin_addr), ipv4_addr_str, sizeof ipv4_addr_str);

	printf("Self IP = %s\n", ipv4_addr_str);
	printf("Socket created\n");
	printf("Socket bound, port %d\n", SERVER_PORT);

	listen(listen_sock, 5);
	printf("Socket listening\n");

	source_size = sizeof source_addr;
	my_sock = accept(listen_sock, (struct sockaddr *)&source_addr, &source_size);
	
	inet_ntop(addr_family, &(source_addr.sin_addr), ipv4_addr_str_client, sizeof ipv4_addr_str_client);
	printf("Socket accepted\n");
	shutdown(listen_sock, SHUT_RDWR);
	return my_sock;
}


/*
* Function Name:	receive_from_send_to_client
* Inputs:			sock [ socket value, if connection is properly created ]
* Outputs: 			None
* Purpose: 			the function receives the data from server and updates the 'rx_buffer'
*					variable with it, sends the obstacle position based on obstacle_pos.txt
*					file and sends this information to the client in the provided format.
* Example call: 	receive_from_send_to_client(sock);
*/
int receive_from_send_to_client(int sock){
	static char obs[5][3][10] ; // 5 mazes 3 obstacles at most, 10 max string size of each obs
	static int i, j, first_run=1, demo_run=1;
	static char final_msg[] = "@$@";
	if (first_run){
		first_run = 0;
		parse_obstacles(obs);
	}
	
	if (i>=5){
		printf("________________________________________\n");
		printf("Connection closed\n");
		printf("Shutting down socket\n");
		shutdown(sock, SHUT_RDWR);
		exit(0);
	}

	memset(rx_buffer, 0, RX_BUFFER_SIZE);
	recv(sock, rx_buffer, RX_BUFFER_SIZE, 0);

	printf("________________________________________\n");
	printf("Received %d bytes from  %s:\n", strlen(rx_buffer), ipv4_addr_str_client);
	printf("Data Received = %s\n", rx_buffer);
	if ((*obs[i][j] == '\0') || (j>=3)){
		i++;
		j=0;
		strcpy(tx_buffer, final_msg);
		if (demo_run){
			demo_run = 0;
			i=0;
			j=0;
		};
	}
	else{
		strcpy(tx_buffer, obs[i][j++]);
	}

	printf("Transmitted %d bytes: %s:\n", strlen(tx_buffer), tx_buffer);
	send(sock, tx_buffer, strlen(tx_buffer), 0);
	fflush(stdout);


	return 0;

}


/*
* Function Name:	main()
* Inputs:			None
* Outputs: 			None
* Purpose: 			the function solves Task 1B problem statement by making call to
* 					functions socket_create() and receive_from_send_to_client()
*/
int main() {
	
    char *input_file_name = "obstacle_pos.txt";
	char *output_file_name = "data_from_client.txt";

	// Create socket and accept connection from client
	int sock = socket_create(dest_addr, source_addr);

	input_fp = fopen(input_file_name, "r");

	if (input_fp == NULL){
		printf("Could not open file %s\n",input_file_name);
		return 1;
	}

	fgets(line_data, MAXCHAR, input_fp);

	output_fp = fopen(output_file_name, "w");

	if (output_fp == NULL){
		printf("Could not open file %s\n",output_file_name);
		return 1;
	}

	while (1) {

		// Receive and send data from client and get the new shortest path
		receive_from_send_to_client(sock);

		// NOTE: YOU ARE NOT ALLOWED TO MAKE ANY CHANGE HERE
		fputs(rx_buffer, output_fp);
		fputs("\n", output_fp);

	}

	return 0;
}

