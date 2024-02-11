# Project description
![Project picture](https://github.com/Lumberj3ck/new_manga_reader/blob/main/reader/static/favicons/android-chrome-192x192.png)  

[Project online](https://mangalove.site/)  
📖 Extensive Manga Library: Platform where people can read their favorite manga.

📚 Chapter Bookmarks: Users can bookmark and save their progress within manga chapters, making it easy to pick up where they left off.

💬 Interactive Comments: We encourage lively discussions with an integrated comment system. Readers can share their thoughts, theories, and reactions on each chapter.

🔎 Advanced Search: Finding specific manga titles or genres is a breeze with our advanced search and filter options, enhancing the user's overall experience.

📱 Responsive Design: The platform is fully responsive, ensuring an optimal reading experience on desktops, tablets, and mobile devices.

📖 Reader-Friendly Interface: The reader interface is designed for ease of use, allowing users to navigate chapters effortlessly.

🔒 User Profiles: Users can create profiles, customize avatars, and keep track of their reading history.

## Technologies Used:

Frontend: HTML5, CSS3, JavaScript 

Backend: Django

Database: PostgreSQL

Deployment: AWS

How to use:
Check the cloudflare for dns and change it for new server ip
1. Edit .env.prod file add your site ip or domain name to allowed host variable
2. Enable docker
  ```
   docker compose build
   docker compose up
   ```
4. Then you need to create a volume for postgres to implement this run this command. This code bellow will create data for database from db.json file.  
  ```
    docker exec your_container_id python manage.py migrate
    docker exec your_container_id python manage.py loaddata db.json
  ```
5. Enable search, Inside postgres shell 
  ```
   psql -U yourusername -d yourdatabase
    # psql -U lumberjack -d manga_project
  ```
6. Inside psql shell run
  ```
 CREATE EXTENSION pg_trgm;
  ```
(Check the ssl guide](https://github.com/Lumberj3ck/SSL-on-Nginx/tree/main)
Now set up is done
