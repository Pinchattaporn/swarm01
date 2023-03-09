# swarm01 fastapi
Ref. awaresome-compose
    
- https://github.com/docker/awesome-compose/tree/master/fastapi

Wakatime project
- https://wakatime.com/@spcn07/projects/wzcblnafge?start=2023-02-27&end=2023-03-05

Url fastapi
- https://spcn07fastapi.xops.ipv9.xyz/


## ขั้นตอนการสร้าง
 - [1.สร้างและใช้งาน Vm](#1สร้างและใช้งาน-vm)
 - [2.Stack และ Portainer](#2portainer)
 - [3.Revert proxy](#3revert-proxy)
 - [4.Images On Dockerfile](#4images-on-dockerfile)
 - [5.Create fastapi](#5create-fastapi)

 # 1.สร้างและใช้งาน Vm
- สร้าง Vm เบื้องต้นดูได้ที่
   * https://github.com/Pinchattaporn/SPCN-011
   * Vm spec
        * Ubuntu 22.04
        * CPU 2 cores
        * Ram 2 GB
        * HDD 32 GB

- เมื่อสร้าง Vm เสร็จแล้วทำการ clone ออกมา 3  Node ได้แก่
    * mannger (spcn07-manager)
    * work1 (spcn07-worker1)
    * work2 (spcn07-worker2)

- ทำการ Set Hostname ใหม่ ด้วยคำสั่ง
    *  hostnamectl set-hostname " ชื่อชื่อใหม่ที่เราต้องการตั้ง"
        * hostname ใหม่ของดิฉัน ได้แก่
            * spcn07-manager
            * spcn07-worker1
            * spcn07-worker2
- เช็คเลข ip ไม่ให้ซ้ำกันเพื่อทำการ Remote ssh ที่ Vscode
    * ติดตั้ง Extension ที่เกี่ยวกับงาน(ssh,wakatime)
    * เชื่อม ssh ไปยัง Vm ที่เราจะทำ Remote ssh
        * ssh root@172.31.1.176 (manager)
        * ssh root@172.31.1.163 (worker1)
        * ssh root@172.31.1.142 (worker2)

# 2.Stack และ Portainer
## Stack
    ในการสร้าง Docker swarm ถ้าสร้างโดยการใช้ CT อาจจะไม่รองรับ swarm ได้ครบถ้วน จึงต้องใช้ Vm แทน
- ติดตั้ง swarm โดยใช้คำสั่ง
    * docker swarm init (Node แรกของคลัสเตอร์)
       * จะได้ Url token มาแล้วเอาไป Run บน Worker Node พอเรารันเสร็จเราจะทราบว่าการ joy สมบูรณ์มั้ย
- ทำการ add worker to this swarm
    * docker node Is : เช็ครายการ Node ที่ทำการเชื่อมต่อ
    
  ผลลัพธ์

  ![Picture2](images/Picture2.png)
## Portainer
- ติดตั้ง Portainer CE

        curl -L https://downloads.portainer.io/ce2-17/portainer-agent-stack.yml -o portainer-agent-stack.yml

        docker stack deploy -c portainer-agent-stack.yml portainer 
   
   * Copy Command แล้วนำไปรันในเครื่อง Vm ทั้ง 3 Node ที่สร้างไว้ในข้อที่ผ่าน และทำการ deploy

 * ผลลัพธ์ 
    - เกิดการสร้าง Service 2 service

    
      ![portainer](images/portainer.png)

- เช็คโดยการเข้าใช้ Url
    * https://172.31.176:9443

    * ผลลัพธ์
![Url](images/Url.jpg)

 # 3.Revert proxy
 - ทำการรันคำสั่ง
    * สร้าง Network มารองรับ

            docker network create --driver=overlay traefik-public

    * ตรวจสอบ Network ที่ถูกสร้างใหม่

            docker network ls 
        
        * ผลลัพธ์


        ![node ls](images/node%20ls.png)

        * เช็คว่า Network ถูกสร้างสำเร็จมั้ยที่ 
        
                Portainer -> Network -> TRAEFIK-PUBLIC
            * ผลลัพธ์

       ![traefik](images/traefik.png)

- สร้าง label
    * Get ID Node

           export NODE_ID=$(docker info -f '{{.Swarm.NodeID}}') 
           echo $NODE_ID

    * สร้าง label


            docker node update --label-add traefik-public.traefik-public-certificates=true $NODE_ID

        <center><img src="images/label.png" alt="center"></center>


    * ปรับเปลี่ยนข้อมูล traefik ก่อนที่จะ export
        
        ```
        export EMAIL=user@smtp.com
        export DOMAIN=traefik.cpedemo.local
        export USERNAME=admin
        export PASSWORD=changeMe
        export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)
        echo $HASHED_PASSWORD
        ```
    
    * ตัวอย่างการ set ข้อมูล

    ![set traefik](images/set%20traefik.png)

    * ตัวอย่างผลลัพธ์ การ export

    ![run](images/run.png)

- ทำการ deploy treafik stacks
    
        docker stack deploy -c traefik- host.yml traefik

    * Befor & After 
           
         * มีการเพิ่มของ Stack traefik

        ![Portainer Before](images/Poratiner%20Before.png)

    

       ![Portainer After](images/Portainer%20After.png)

- ดูผลลัพธ์ที่ Url
    * http://traefik.cpedemo.local
    
    ![Dsh-traefik](images/Dsh-traefik.png)

# 4.Images On Dockerfile
- build image จาก Dockerfile

        docker build . -t chattaporn/fastapi:v1
       
        โดย chattaporn/fastapi คือ path App ใน DockerHub

- push image ขึ้น DockerHub

        docker push chattaporn/fastapi


 # 5.Create fastapi

- ทำการ Clone github จาก
  Ref.
  
    - https://github.com/docker/awesome-compose/tree/master/fastapi

  
  ![folder](images/folder.png)
  ![infolder](images/in%20folder.png)

- ทำการแก้ไขข้อมูลไฟล์ main.py


<center><img src="images/main.png"></center>


  - โดยเข้าไปที่ app -> main.py -> แก้ไขข้อความตรง message: สวัสดีค่ะหนูชื่อ ฉัตรพร แก้วเฉลิม

<center><img src="images/set.png"></center>

- build images 

  - โดยการเข้าที่ Docker hub -> Create repository -> ตั้ง Name = fastapi

<center><img src="images/build.png" alt="center"></center>
<center><img src="images/finish.png" alt="center"></center>

- copy path:  chattaporn/fastapi

        โดยใช้คำสั่ง  
         docker build . -t chattaporn/fastapi:v1

- push ขึ้น Dockerhub
    * ใช้คำสั่ง docker login เพื่อเข้าสู่ระบบก่อน
    * ใช้คำสั่ง docker push chattaporn/fastapi

<center><img src="images/8023.png" alt="center"></center>
    
    * ผลลัพธ์จากรัน
      
<center><img src="images/images-hub.png" alt="center"></center>

- แก้ไขข้อมูล docker-compose.yaml

    <center><img src="images/Cap-code.png" alt="center"></center>

- deploy stack 
     
     * https://portainer.ipv9.me/

 
        โดยทำการ กด Aff Stack -> ตั้งชื่อ fastapi-spcn07 -> วางโค้ด docker-  compose.yaml ที่ wab editor -> Deploy the stack

    <center><img src="images/Add-st.png" alt="center"></center>

    <center><img src="images/Create.png" alt="center"></center>

    <center><img src="images/stack2.png" alt="center"></center>

* ผลลัพธ์จากการ deploy stack

   
    <center><img src="images/Adfast.png" alt="center"></center>

- เช็คว่า Url เข้าใช้งานได้จริงมั้ย แสดงผลจริงมั้ย

    * https://spcn07fastapi.xops.ipv9.xyz/

    * ผลลัพธ์

    <center><img src="images/ผลลัพธ์.png" alt="center"></center>

Ref.ทั้งหมด
 
 * https://github.com/pitimon/dockerswarm-inhoure/tree/main/ep03-traefik

 * https://github.com/pitimon/dockerswarm-inhoure

 