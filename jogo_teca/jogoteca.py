from flask import Flask, render_template, request, redirect, session,flash,url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo("Tetris", "Puzzle", "Atari")
jogo2 = Jogo("Valorant", "FPS", "PC")
jogo3 = Jogo("Elden Ring", "MMORPG", "PC")
lista = [jogo2, jogo1, jogo3]

class Usuario:
    def __init__(self,nome,nickname,senha):
        self.nome=nome
        self.nickname=nickname
        self.senha=senha
usuario1=Usuario("José Carlos","jcms","zezim")
usuario2=Usuario("Maria Fernanda","nana","1234")
usuario3=Usuario("Luiz Pierre","pit","pitbull1234")

usuarios={ usuario1.nickname : usuario1,
           usuario2.nickname : usuario2,
           usuario3.nickname : usuario3}



app = Flask(__name__)
app.secret_key="12345"

@app.route("/")
def index():
    return render_template("lista.html", titulo="Jogos", lista_jogos=lista)

@app.route("/novo")
def novo():
    if "usuario_logado" not in session or session["usuario_logado"]==None:
        return redirect(url_for("login", proxima=url_for("novo")))

    return render_template("novo.html", titulo="Novo Jogo")

@app.route('/criar', methods=['post'])

def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for("index"))

@app.route("/login")
def login():
    proxima = request.args.get("proxima")
    return render_template("login.html", proxima=proxima)

@app.route("/autenticar", methods=["POST"],)
def autenticar():
    if request.form["usuario"] in usuarios:
        usuario=usuarios[request.form["usuario"]]
        if request.form["senha"]== usuario.senha:
            session["usuario_logado"]=usuario.nickname
            flash(session["usuario_logado"] + " logado com sucesso!")
            proxima_pagina = request.form["proxima"]
            return redirect(proxima_pagina)
        else:
            flash("Usuario nao logado")
            return  redirect(url_for("login"))

@app.route("/logout")
def logout():
    session["usuario_logado"]=None
    flash("Logout efetuado com sucesso!")
    return redirect(url_for("index"))



app.run(debug=True)
