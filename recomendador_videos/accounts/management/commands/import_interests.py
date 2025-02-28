from django.core.management.base import BaseCommand
from ...models import Interest

class Command(BaseCommand):
    help = 'Importa áreas de interesse a partir de um arquivo txt com hierarquia representada pela identação do arquivo'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Caminho do arquivo txt')

    def build_tree(self, lines):
        root = {}
        stack = [(root, -1)]
        
        for line in lines:
            level = len(line) - len(line.lstrip())
            name = line.strip()
            
            if not name:
                continue
            while stack and stack[-1][1] >= level:
                stack.pop()
            node = {}
            stack[-1][0][name] = node
            stack.append((node, level))
        
        return root

    def save_tree(self, tree, parent=None):
        for name, children in tree.items():
            interest, created = Interest.objects.get_or_create(name=name, parent=parent)
            
            if created:
                path = self.get_interest_path(interest)
                self.stdout.write(self.style.SUCCESS(f'Interesse "{path}" adicionado com sucesso!'))
            else:
                self.stdout.write(self.style.WARNING(f'Interesse "{name}" já existe no nível correto.'))
            self.save_tree(children, parent=interest)
    
    def get_interest_path(self, interest):
        path = []
        while interest:
            path.insert(0, interest.name)
            interest = interest.parent
        return ' > '.join(path)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                tree = self.build_tree(lines)
                
                self.stdout.write(self.style.SUCCESS('Árvore de interesses montada com sucesso! Salvando no banco...'))
                self.save_tree(tree)
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado: {file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro: {e}'))
