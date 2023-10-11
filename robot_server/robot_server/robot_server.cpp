#include <iostream>
#include <string>
#include <WS2tcpip.h>
#include <json/json.h>

#pragma comment (lib, "ws2_32.lib")

int main()
{
    // Initialize Winsock
    WSADATA wsData;
    WORD ver = MAKEWORD(2, 2);

    // Attempt to start up winsock.
    int wsResult = WSAStartup(ver, &wsData);

    // If winsock failed to start, throw an exception.
    if (wsResult != 0)
    {
        std::cerr << "Can't start Winsock, Err #" << wsResult << std::endl;
        return -1;
    }

    // Create a socket and define its protocols.
    SOCKET listening = socket(AF_INET, SOCK_STREAM, 0);

    // If the socket is invalid, throw an exception.
    if (listening == INVALID_SOCKET)
    {
        std::cerr << "Can't create socket, Err #" << WSAGetLastError() << std::endl;
        return -1;
    }

    std::cout << "created server";
        
    // Bind the IP address and port to a socket
    sockaddr_in hint;
    hint.sin_family = AF_INET;

    // Define the port to be bound to the socket (static).
    hint.sin_port = htons(2345);
    hint.sin_addr.s_addr = INADDR_ANY;
    bind(listening, (sockaddr*)&hint, sizeof(hint));

    // Begin listening on the socket.
    listen(listening, SOMAXCONN);

    // Receive client connection
    sockaddr_in client;
    int clientSize = sizeof(client);

    // Accept the client connection and store the client socket.
    SOCKET clientSocket = accept(listening, (sockaddr*)&client, &clientSize);

    // Retrieve the host information from the socket.
    char host[NI_MAXHOST];
    char service[NI_MAXSERV];

    ZeroMemory(host, NI_MAXHOST);
    ZeroMemory(service, NI_MAXSERV);

    if (getnameinfo((sockaddr*)&client, sizeof(client), host, NI_MAXHOST, service, NI_MAXSERV, 0) == 0)
    {
        std::cout << host << " connected on port " << service << std::endl;
    }
    else
    {
        inet_ntop(AF_INET, &client.sin_addr, host, NI_MAXHOST);
        std::cout << host << " connected on port " << ntohs(client.sin_port) << std::endl;
    }

    // Close listening socket
    closesocket(listening);

    // While loop: accept and echo message back to client
    char buf[4096];
    while (true)
    {
        ZeroMemory(buf, 4096);

        // Receive data from the client
        int bytesReceived = recv(clientSocket, buf, 4096, 0);

        // If the socket fails, throw an error.
        if (bytesReceived == SOCKET_ERROR)
        {
            std::cerr << "Error in recv(). Quitting" << std::endl;
            break;
        }

        // If the client disconnected, throw an error.
        if (bytesReceived == 0)
        {
            std::cout << "Client disconnected" << std::endl;
            break;
        }

        // Echo message back to client
        send(clientSocket, buf, bytesReceived + 1, 0);
    }

    // Close the socket
    closesocket(clientSocket);

    // Cleanup Winsock
    WSACleanup();

    return 0;
}

