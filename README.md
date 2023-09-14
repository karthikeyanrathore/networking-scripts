# Networking Topics
* [OSI model](#OSI model)


# OSI model
* Standard model for communication among different devices of different versions, operation sys etc.
* 7 Layers 
	* Application layer: 
		* initiate communication
		* (HTTP/FTP/SMTP/DHCP)
	* Presentation layer: 
		* prepare data in a correct format so, that the server/client can understand.
		* For example if client is sending JSON data to server, then this layer will serialize client JSON to flat byte strings.
	* Session layer:
		* synchronizes data transfer with checkpoints: https://www.cloudflare.com/en-gb/learning/ddos/glossary/open-systems-interconnection-model-osi/
	* Transport layer:
		* TCP/UDP
	
