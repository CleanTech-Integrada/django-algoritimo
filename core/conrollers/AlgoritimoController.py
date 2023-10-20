from core.services.geneticAlgorithm import PopulationGenerator, NaturalSelection
from core.services.presentation import Graphics
from django.http import JsonResponse
import json
from django.templatetags.static import static


def index(request):
    coords = request.GET.get('coords', '{}')

    # Configurações
    population_size = 100
    mutation_rate = 0.1
    arena_size = 40
    graphics_width = 15
    graphics_height = 8
    generations = 25
    routes_to_plot = 1


   # Leitura de arquivos
    with open(static('../../template/static/distances.json'), "r") as read_file:
        distance = json.load(read_file)

    with open(static("../../template/static/coordinates.json"), "r") as read_file:
        coordinates = json.load(read_file)

    with open(static("../../template/static/names.json"), "r") as read_file:
        name = json.load(read_file)
    print('Bem vindo ao problema do caixeiro viajante com algoritmo genético!')

    # Pega lista de cidades
    city_list = list(coordinates.keys())

    # População inicial
    initial_population = PopulationGenerator(population_size, city_list).generatePopulation()

    # Inicia os modelos de lógica e apresentação
    model = NaturalSelection(distance, initial_population)
    graphics = Graphics(routes_to_plot, generations, coordinates, name, graphics_width, graphics_height)

    # Liga o modelo de apresentação ao lógico, para que ele receba os relatório de progresso
    model.subscribe(graphics.receiveData)

    # Salva o custo antigo
    old_cost = model.getFitness()[model.getFittest()]

    # Mostra a rota e custo inicial
    old_fittest = model.population[model.getFittest()]
    print(
        f'\nO melhor indivíduo da geração inicial faz a rota: {graphics.describeRoute(old_fittest)}\nSeu custo é: {old_cost}\nRota em lista: {old_fittest}')

    # Executa a evolução
    the_fittest = model.geneticAlgorithm(generations, arena_size, mutation_rate, True)

    # Gera o gráfico
    # graphics.generateGraph()

    # Pega o custo final do modelo
    final_cost = model.getFitness()[model.getFittest()]

    # Mostra a rota e custo final
    # print(
    #     f'\nO melhor indivíduo da geração final faz a rota: {graphics.describeRoute(the_fittest)}\nSeu custo é: {final_cost}\nRota em lista: {the_fittest}')

    # graphics.display()
    return JsonResponse({'data':  coords})


