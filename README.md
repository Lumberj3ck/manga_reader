# Manga Love: Explore, Read, Enjoy

![Manga Love](https://github.com/Lumberj3ck/new_manga_reader/blob/main/reader/static/favicons/android-chrome-192x192.png)

[Visit Manga Love](https://mangalove.site/)

## Description

Manga Love is an simple manga library, providing readers with a platform to explore, read, and enjoy their favorite manga series. With a user-friendly interface and a wide selection of titles, Manga Love aims to be the go-to destination for manga lovers.

## Motivation

The motivation behind Manga Love stems from a passion for manga and a desire to create a hub where readers can enjoy their favorite titles. By offering features like chapter bookmarks, interactive comments, advanced search, and user profiles, Manga Love seeks to enhance the reading experience.

## Quick Start

To start using Manga Love quickly, follow these steps:

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

## Usage

**Manga Library**: Platform where people can read their favorite manga.

**Chapter Bookmarks**: Users can bookmark and save their progress within manga chapters, making it easy to pick up where they left off.

**Interactive Comments**: We encourage lively discussions with an integrated comment system. Readers can share their thoughts, theories, and reactions on each chapter.

 **Search**: Finding specific manga titles or genres is a breeze with our advanced search and filter options, enhancing the user's overall experience.

**Responsive Design**: The platform is fully responsive, ensuring an optimal reading experience on desktops, tablets, and mobile devices.

**Reader-Friendly Interface**: The reader interface is designed for ease of use, allowing users to navigate chapters effortlessly.

**User Profiles**: Users can create profiles, customize avatars, and keep track of their reading history.
