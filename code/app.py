from flask import Flask

app = Flask(__name__)


@app.route("/", methods=['GET'])
def root():
    return "Bem vindo a fabulosa locadora de carros de luxxxo da Raquel!"


if (__name__ == "__main__"):
    app.run()
