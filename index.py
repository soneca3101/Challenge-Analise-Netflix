from flask import Flask, render_template
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

# Função para carregar dados e gerar gráficos
def create_plots():
    # Carregar o dataset
    df = pd.read_csv('netflix_titles.csv')

    # Gráfico 1: Contagem de filmes por país
    countries_count = df['country'].value_counts().head(10)
    plt.figure(figsize=(10, 5))
    countries_count.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Países com Mais Produções')
    plt.ylabel('Número de Produções')
    plt.tight_layout()
    plt.savefig('static/countries_count.png')  
    plt.close()

    # Gráfico 2: Diretores com mais filmes
    directors_count = df['director'].value_counts().head(5)
    plt.figure(figsize=(8, 4))
    directors_count.plot(kind='bar', color='green')
    plt.title('Top 5 Diretores com Mais Produções')
    plt.ylabel('Número de Produções')
    plt.tight_layout()
    plt.savefig('static/directors_count.png')
    plt.close()

    # Gráfico 3: Quantos filmes estão disponíveis na Netflix?
    num_movies = df[df['type'] == 'Movie'].shape[0]
    plt.figure(figsize=(8, 4))   
    plt.bar(0, num_movies, color='orange')   
    plt.title('Quantidade de Filmes na Netflix')
    plt.ylabel('Número de Filmes')
    plt.tight_layout()
    plt.savefig('static/num_movies.png')
    plt.close()

    # Gráfico 4: Quais diretores também atuaram como atores em suas próprias produções?
    df_directors_actors = df.dropna(subset=['director', 'cast'])
    directors_actors = df_directors_actors[df_directors_actors.apply(lambda row: any(
        actor in row['director'] for actor in row['cast'].split(',')), axis=1)]
    plt.figure(figsize=(8, 4))
    directors_actors.plot(kind='bar', x='director', y='title', color='purple')
    plt.title('Diretores que Atuaram como Ator')
    plt.ylabel('Número de Filmes')
    plt.tight_layout()


# Rota principal para o dashboard
@app.route('/')
def dashboard():
    # Chama a função para criar gráficos
    create_plots()
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
