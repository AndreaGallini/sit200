import importlib
import os
import re
import json
import concept

exclude_files = ['__init__.py', 'pipeline.py', 'emissionreduction.py']

for file in os.listdir('ao1'):
    if file.endswith(".py") and file not in exclude_files:
        module_name = file[:-3]
        if module_name != '__init__':
            importlib.import_module(module_name)
            print(f'Imported module {module_name}')

class Model:
    def __init__(self, name, script_name, input_data, output_data, dependencies):
        self.name = name
        self.script_name = script_name
        self.input_data = input_data
        self.output_data = output_data
        self.dependencies = dependencies

class ModelCatalog:
    def __init__(self, directory):
        self.models = []
        for filename in os.listdir(directory)   :
            if filename.endswith(".py"):
                filepath = os.path.join(directory, filename)
                class_name = None
                input_keys = []
                output_keys = []
                inside_init = False
                collecting_input = False
                collecting_output = False
                input_buffer = ""
                output_buffer = ""
                with open(filepath, 'r') as file:
                    for line in file:
                        class_match = re.match(r'class\s+(\w+)\(', line)
                        if class_match:
                            class_name = class_match.group(1)
                        if re.match(r'\s*def\s+__init__', line):
                            inside_init = True
                            continue
                        if inside_init:
                            if re.match(r'\s*def\s+\w+', line) or re.match(r'\s*class\s+\w+', line):
                                inside_init = False
                            if 'self.input' in line:
                                collecting_input = True
                                input_buffer = ""  
                            elif 'self.output' in line:
                                collecting_output = True
                                output_buffer = ""  
                            if collecting_input:
                                input_buffer += line
                                if '}' in line:  
                                    collecting_input = False
                                    input_keys = re.findall(r'[\'"]([^\'"]+)[\'"]\s*:', input_buffer)
                            if collecting_output:
                                output_buffer += line
                                if '}' in line:  
                                    collecting_output = False
                                    output_keys = re.findall(r'[\'"]([^\'"]+)[\'"]\s*:', output_buffer)
                    self.models.append((filename[:-3], class_name, input_keys, output_keys,[]))
        self.models.sort(key=lambda x: x[0])
        for i, item in enumerate(self.models):
            for output_key in item[3]:
                for j, other_item in enumerate(self.models):
                    if i == j:
                        continue
                    if output_key in other_item[2]:
                        self.models[j][4].append(item[0])
        with open('models_catalog.json', 'w') as json_file:
            json.dump([{
            'filename': item[0],
            'class_name': item[1],
            'input_keys': item[2],
            'output_keys': item[3],
            'dependencies': item[4]
            } for item in self.models], json_file, indent=4)

    def get_model_input(self, model_name):
        for model in self.models:
            if model[1] == model_name:
                return model[2]
        return None

    def get_model_dependencies(self, model_name):
        for model in self.models:
            if model[1] == model_name:
                return model[3]
        return None


class AO1Pipeline:
    def __init__(self):
        self.pipeline = []
        models_catalog = concept.ModelCatalog("ao1")

    def add_model(self, model):
        '''
        This method adds a model to the pipeline
        input: model, the model to be added
        output: boolean, True if the model has been added, False otherwise
        after adding the model, the model input data is checked
        add_model() and check_model_input() are mutually recursive
        '''
        pass

    def check_model_input(self, model):
        '''
        This method checks if the input data for the model is available
        input: model, the model to be checked
        output: boolean, True if the input data is available, False otherwise
        add_model() and check_model_input() are mutually recursive
        '''
        # Get the input parameters names for the model
        # Check if there is a dependency to another model
        # If there is a dependency, add the model to which the dependency refers to the pipeline 
        # If there is no dependency, check if the input data is available
        # If the input data is available, return True
        # If the input data is not available, return False and stop the pipeline
        pass

    def check_pipeline(self):
        '''
        This method checks if the pipeline is correct (avoid circular dependencies)
        output: boolean, True if the pipeline is correct, False otherwise
        '''
        pass

    def run(self):
        '''
        This method runs the pipeline
        each model is executed in sequence and the output data is stored in the DataBank
        if the input data is not available, the pipeline will stop
        if the output data has already been computed, the model will not be executed
        '''
        db = self.DataBank()
        for model in self.pipeline:
            input_data = db.get_input(model)
            model.run(input_data)
            output_data = model.get_output()
            db.set_output(model, output_data)

class DataBank:
    '''
    This class is used to store input data for the pipeline
    input: dictionary, input data for each model
    output: dictionary, output data for each model
    '''
    def __init__(self):
        self.data = []

    def get_input(self, model):
        return self.data

    def set_input(self, model, input_data):
        self.data = input_data

    def get_output(self, model):
        return self.data
            
    def set_output(self, model):
        pass


if __name__ == '__main__':
    #pipeline = AO1Pipeline()
    #pipeline.add_model('energyindependencefactor')
    #databank = DataBank()
    #energyindependencefactor_input = {'self_consumed_energy': 0.5, 'total_energy_consumed': 1.0}
    #databank.set_input('energyindependencefactor', energyindependencefactor_input) 
    #pipeline.add_model('energyindependencefactor')
    #pipeline.run()
    model_catalog = ModelCatalog('ao1')