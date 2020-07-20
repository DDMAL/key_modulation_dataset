#!/usr/bin/env python
# coding: utf-8

import utils
import pandas as pd

# Evaluable datasets
datasets = [
    'aldwell', 
    'kostka-payne',
    'reger',
    'rimsky-korsakov', 
    'tchaikovsky',
    'all_files'
]

models = [
    'random_guess',
    'globalkey_guess',
    'justkeydding',
    'perfect_modulation',
    'perfect_tonicization',
    # 'laurent'
]

# Tasks to evaluate
task_dict = {
    'modulation': 'local_key_label', 
    'tonicization': 'tonicized_key_label'
}

def score_slice(evaldfrow):    
    gt, pred, _ = evaldfrow
    score = utils.score_key_prediction(gt, pred)
    return score

def score_slice_with_duration(evaldfrow):
    gt, pred, dur = evaldfrow
    score = utils.score_key_prediction(gt, pred) * dur
    return score

# Evaluation metric
evaluation_metrics = {
    'duration_based': score_slice_with_duration,
    'slice_based': score_slice
}

def get_model(name, dataset_name, dfm, dft):
    if name == 'random_guess':
        return utils.generate_random_predictions(dataset_name)
    elif name == 'globalkey_guess':
        return utils.generate_globalkey_predictions(dataset_name)
    elif name == 'justkeydding':
        return utils.justkeydding_to_dfdictionary(f'{dataset_name}_justkeydding.tsv')
    elif name == 'perfect_modulation':
        # _, dfm, _ = utils.load_dataset(dataset)
        return dfm
    elif name == 'perfect_tonicization':
        # _, _, dft = utils.load_dataset(dataset)
        return dft
    elif name == 'laurent':
        ''' TODO: implement laurents '''

def pass_sanity_check(df, model):
    errors = 0
    for f in list(df.keys()):
        if not df[f].index.equals(model[f].index):
            print(f"Warning. Index of file {f} doesn't match the index of ground truth")
            print(df[f].index.difference(model[f].index))
            errors += 1
    return (errors == 0)

# Iterating in the following fashion
#   all_files
# 	    modulation
#    		justkeydding
# 	    		slice-based
#    			duration-based
# 		    perfect_tonicization
# 			    slice-based
# 			    duration-based
# 		    ...
# 	    tonicization
# 		    ...
#   aldwell
# 	...
def evaluate_all():
    scorelist = []    
    for dataset_name in datasets:
        # Load the dataset only once (because it is slow)
        df, dfm, dft = utils.load_dataset(dataset_name)        
        for task_name in task_dict.keys():            
            for model_name in models:
                for evaluation_name in evaluation_metrics.keys():                                
                    task = task_dict[task_name]
                    model = get_model(model_name, dataset_name, dfm, dft)
                    evaluation = evaluation_metrics[evaluation_name]
                    if not pass_sanity_check(df, model):
                        print(f"Can't evaluate model ${model_name}. Indexes are not correct.")
                        quit()                    
                    
                    for f in list(df.keys()):
                        # Create the evaluation dataframe
                        dfeval = pd.DataFrame(index=df[f].index)
                        dfeval['gt'] = df[f][task]
                        dfeval['pred'] = model[f].local_key_label
                        dfeval['slice_duration'] = df[f].slice_duration    
                        dfeval['score'] = dfeval.apply(evaluation, axis=1, raw=True)
                        if evaluation_name == 'slice_based':
                            score = dfeval['score'].sum() / dfeval.index.size
                        elif evaluation_name == 'duration_based':
                            score = dfeval['score'].sum() / dfeval.slice_duration.sum()
                        scorelist.append({
                            'dataset': dataset_name,
                            'file': f,
                            'task': task_name,
                            'model': model_name,
                            'evaluation': evaluation_name,                            
                            'mirex_score': score 
                        })                        
                    # scoredf = pd.DataFrame(scoredict.values())
                    # print(scoredf.mean(), scoredf.std(), scoredf.min(), scoredf.max())
    return scorelist



