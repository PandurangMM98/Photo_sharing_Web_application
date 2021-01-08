# Photo_sharing_Web_application

Description:
The Application name is Selfieless act. which means uploading photos of helping people , feeding animals , social work etc..
I used Html,Css and Python for the front end.Main intention was Back end work, which used Python Flask web Framework, Rest API
use the HTTP protocol Request and Response mechanism, JSON for storing the data , Microservices which software divided
in small independent services communicate over APIs. I created 2 independent services one was user and another was acts .
I created 10 Rest APIs which are add user , remove user , add category , remove category , list of categories, upload
acts(act id,username, image, caption, date), size of acts inside category, upvote for act, downvote. All this data is stored in a JSON file.
API requests are POST, GET, DELETE, PUT. HTTP Responses are 200(ok), 201(created) ,400(Bad request), 404(not found), 405(method not allowed) etc..
Postman used for verifying APIs are working properly or not like Requests and http responses. Docker containers are lightweight and can build, maintain,
ship and deploy your application. web application hosted on aws server. created 2 EC2 instances one for user and another for acts. 
Load balancer which distributes incoming application traffic across EC2 instances. Fault tolerance is the ability that enables a system
to continue operating properly in the failure of some microservice components.
I did this project in a short time. So still i have to work  more on Docker, containers,hypervisor, scale up, scale down.
