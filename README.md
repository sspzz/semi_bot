![Twitter_HQ_1500x500-2](https://user-images.githubusercontent.com/91800037/157248754-78e24061-f47c-44f7-8686-87818f02bbb7.png)


# 🦹🏼‍♀️ SemiBot

A simple Discord Bot which will, among other things, download and display artwork for any given SemiSuper from [SemiSupers](https://semisupers.com).

## 🤖 Commands

- `!gm` - Semi GM!
- `!gn` - Semi GN!
- `!semi`- Semi with traits and rarites
- `!pfp` - Original artwork
- `!tpfp` - Original artwork on transparent background
- `!head` - Just the SemiSuper's head
- `!thead` - Just the SemiSuper's head on transparent background
- `!say` - Create catchprases for your SemiSuper
- `!vs` - Pitch SemiSupers into battle

## 📸 Examples

![5295-gm](https://user-images.githubusercontent.com/91800037/157320323-e7cc1fa1-88cb-48a3-8d8b-593167456e20.png)
![2347-gn](https://user-images.githubusercontent.com/91800037/157320441-d4bb78fe-1367-4e17-87a1-f732dd13ed17.png)
![5340-head](https://user-images.githubusercontent.com/91800037/157322065-fce6f8ea-98f1-40d9-b943-2a6cd92ba019.png)![271-head](https://user-images.githubusercontent.com/91800037/157322104-70b9383a-b3f9-44b2-855d-870ba1164d70.png)
![1984-catchphrase](https://user-images.githubusercontent.com/91800037/157414243-21c70c21-83c9-4fed-9b0f-09e14df855a7.png)
![5340-vs](https://user-images.githubusercontent.com/91800037/157413623-c02c4f0a-711e-4c40-9901-21deaf814010.png)

## 🖥 CLI

You can use this as a stand-alone tool for downloading and generating artwork; Either supply a list of token IDs as arguments, or run `--all` to generate everything.

For example `$ python3 semi.py 50` will download and generate the artwork for SemiSuper numer 50, aka. Villain #50.

## 📡 REST API

You can run this as a web server providing a RESTful API with the same functionality as the bot itself, just run `$ python3 semi_api.py`.

Onece running, the exposed endpoints are:

- `http://127.0.0.1:5000/semi?tokenId=123`
- `http://127.0.0.1:5000/pfp?tokenId=123`
- `http://127.0.0.1:5000/tpfp?tokenId=123`
- `http://127.0.0.1:5000/head?tokenId=123`
- `http://127.0.0.1:5000/thead?tokenId=123`
- `http://127.0.0.1:5000/gm?tokenId=123`
- `http://127.0.0.1:5000/gn?tokenId=123`
- `http://127.0.0.1:5000/say?tokenId=123&quote=Semi%20hilaroius%20catchphrase`
- `http://127.0.0.1:5000/vs?tokenId=123&tokenId2=321`

