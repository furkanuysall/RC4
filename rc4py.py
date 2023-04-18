import codecs
from flask import Flask, request, send_file

def rc4(key, text):
    S = list(range(256))
    j = 0
    out = []
    key = bytes(key, 'utf-8')
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(char ^ S[(S[i] + S[j]) % 256])
    return bytes(out)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if  request.method == 'POST':
        file = request.files['file']
        text = file.read()
        key = "gizlikey"
        encrypted_data = rc4(key, text)
        with open("sifrelenmis.txt", "wb") as f:
            f.write(encrypted_data)
            key_hex = codecs.encode(key.encode(), 'hex').decode()
            f.write(f'\n{key_hex}'.encode())
        return send_file("sifrelenmis.txt", as_attachment=True)
    else:
        return '''
           
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>RC4 </title>
        <style>
            body{
             font-family: 'Times New Roman', Times, serif;
             margin: 0;
             padding: 0;
             background-color:bisque;
         }
         h1{
             text-align: center;
             margin-top: 75x;
             color:rgb(99, 33, 161);
         }
         h2{
            text-align: center;
            margin: 75x;
            color:rgb(224, 143, 21);
         }
         form{
            margin: 0 auto;
            padding: 20px;
            width: 90%;
            max-width: 400px;
            border:rgb(219, 218, 221);
            background-color: rgb(238, 240, 109);
            box-shadow: 2px 2px 5px red;
         }
         input[type="file"]{
            margin-bottom: 35px;
            

         }
         input[type="submit"]{
            background-color: blanchedalmond;
            color: rgb(238, 140, 59);
            padding: 15px 30px;
            cursor: pointer;
         }
         input[type="submit"]:hover{
            background-color: black;

         }
         
         label{
            font-weight: bold;
            display: block;
            margin-bottom: 15px;
         }
     
         </style>
        
    </head>
    <body>
        <h1>RC4 Şifreleme ve Şifre Çözme</h1>
        <h2>Şifrele</h2>
        <form method="post" enctype="multipart/form-data">
            <label for="enctype-file">Şifrelemek için dosya seçiniz:</label>
            <input type="file" name="file" id="enctype-file">
            <input type="submit" name="submit_button" value="Şifreleme">
        </form>
        <h2>Şifreyi Çözme</h2>
        <form method="post" enctype="multipart/form-data">
            <label for="decrypt-file">Şifrelenmiş dosyayi çözmek için seçiniz:</label>
            <input type="file" name="file" id="decrypt-file">
            <input type="submit" name="submit_button" value="Şifreyi Çöz">
        </form>
    </body>
   
</html>
        '''

if __name__ == '__main__':
    app.run(debug=True)