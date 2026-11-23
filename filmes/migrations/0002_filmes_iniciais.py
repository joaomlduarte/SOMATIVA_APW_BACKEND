"""Cadastra no banco os filmes iniciais do catálogo (o enunciado pede no mínimo 10)."""
from django.db import migrations

FILMES_INICIAIS = [
    {
        'titulo': 'Além das Estrelas',
        'genero': 'Ficção',
        'ano_lancamento': 2024,
        'imagem': 'posters/alem-das-estrelas.svg',
        'sinopse': 'Uma astronauta parte em uma jornada épica para encontrar um novo lar '
                   'para a humanidade, enfrentando o desconhecido nos confins da galáxia.',
    },
    {
        'titulo': 'Velocidade Máxima',
        'genero': 'Ação',
        'ano_lancamento': 2023,
        'imagem': 'posters/velocidade-maxima.svg',
        'sinopse': 'Um piloto de fuga precisa atravessar a cidade em uma única noite para '
                   'salvar o irmão, perseguido por uma gangue implacável.',
    },
    {
        'titulo': 'Entre Mundos',
        'genero': 'Drama',
        'ano_lancamento': 2022,
        'imagem': 'posters/entre-mundos.svg',
        'sinopse': 'Duas irmãs separadas na infância se reencontram e descobrem que suas '
                   'vidas seguiram caminhos completamente opostos.',
    },
    {
        'titulo': 'A Última Expedição',
        'genero': 'Aventura',
        'ano_lancamento': 2021,
        'imagem': 'posters/a-ultima-expedicao.svg',
        'sinopse': 'Um grupo de exploradores escala uma montanha nunca mapeada em busca '
                   'de uma civilização perdida.',
    },
    {
        'titulo': 'O Código Secreto',
        'genero': 'Ação',
        'ano_lancamento': 2020,
        'imagem': 'posters/o-codigo-secreto.svg',
        'sinopse': 'Uma hacker descobre uma conspiração e passa a ser caçada por agentes '
                   'que querem apagar todas as provas.',
    },
    {
        'titulo': 'Rindo à Toa',
        'genero': 'Comédia',
        'ano_lancamento': 2023,
        'imagem': 'posters/rindo-a-toa.svg',
        'sinopse': 'Um padeiro atrapalhado é confundido com um chef famoso e precisa '
                   'comandar a cozinha do restaurante mais exigente da cidade.',
    },
    {
        'titulo': 'Planeta Vermelho',
        'genero': 'Ficção',
        'ano_lancamento': 2019,
        'imagem': 'posters/planeta-vermelho.svg',
        'sinopse': 'A primeira colônia em Marte enfrenta uma tempestade que ameaça cortar '
                   'toda a comunicação com a Terra.',
    },
    {
        'titulo': 'Casamento em Apuros',
        'genero': 'Comédia',
        'ano_lancamento': 2021,
        'imagem': 'posters/casamento-em-apuros.svg',
        'sinopse': 'Às vésperas do casamento, o noivo perde as alianças e tem 24 horas '
                   'para recuperá-las sem que a noiva descubra.',
    },
    {
        'titulo': 'O Peso do Silêncio',
        'genero': 'Drama',
        'ano_lancamento': 2020,
        'imagem': 'posters/o-peso-do-silencio.svg',
        'sinopse': 'Um professor aposentado decide reabrir a escola da sua cidade natal e '
                   'encontra resistência de onde menos espera.',
    },
    {
        'titulo': 'Ilha Perdida',
        'genero': 'Aventura',
        'ano_lancamento': 2024,
        'imagem': 'posters/ilha-perdida.svg',
        'sinopse': 'Após um naufrágio, quatro amigos precisam sobreviver em uma ilha que '
                   'guarda segredos misteriosos.',
    },
    {
        'titulo': 'Fúria nas Ruas',
        'genero': 'Ação',
        'ano_lancamento': 2022,
        'imagem': 'posters/furia-nas-ruas.svg',
        'sinopse': 'Uma policial veterana se une a um jovem novato para desmontar a maior '
                   'quadrilha da cidade.',
    },
    {
        'titulo': 'Memórias do Amanhã',
        'genero': 'Ficção',
        'ano_lancamento': 2025,
        'imagem': 'posters/memorias-do-amanha.svg',
        'sinopse': 'Um cientista cria uma máquina capaz de ler memórias do futuro e '
                   'precisa impedir um desastre que só ele conhece.',
    },
]


def cadastrar_filmes(apps, schema_editor):
    Filme = apps.get_model('filmes', 'Filme')
    for dados in FILMES_INICIAIS:
        Filme.objects.update_or_create(titulo=dados['titulo'], defaults=dados)


def remover_filmes(apps, schema_editor):
    Filme = apps.get_model('filmes', 'Filme')
    Filme.objects.filter(titulo__in=[dados['titulo'] for dados in FILMES_INICIAIS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('filmes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cadastrar_filmes, remover_filmes),
    ]
