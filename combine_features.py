import os
from pprint import pprint
from util import TRAITS, get_trait_scores, z_score_normalize


def read_feature(fp):
    fr = open(fp, 'rU')
    fr.readline()
    id_feature = {}
    for line in fr.readlines():
        items = line.split(',')
        id = items[0]
        features = items[1:-5]
        id_feature[id] = features
    return id_feature

def combine_heuristic_features(feature_names, trait='extra'):
    output_fp = os.path.join('result', 'feature', 'all_heuristic_features_%s.csv' % trait)
    input_dir = os.path.join('result', 'feature')
    labels = ['uid']
    for feature_name in feature_names:
        if '-' in feature_name:
            labels.extend(feature_name.split('-'))
        else:
            labels.append(feature_name)
    id_y = get_trait_scores(trait)  
    ids = sorted(id_y.keys())
    all_features = {id:[] for id in ids}
    for feature_name in feature_names:
        fp = os.path.join(input_dir, '%s.csv' % feature_name)
        id_feature = read_feature(fp)
        for id in all_features:
            if id in id_feature:
                all_features[id].extend(id_feature[id])

    fw = open(output_fp, 'a')
    labels.append(trait)
    fw.write(','.join(labels) + '\n') 
    for id in ids:
        line = [id]
        line.extend(all_features[id])
        line.append(id_y[id])
        fw.write(','.join(line) + '\n') 
    fw.close()
        
def combine_freq_patterns(support, normalize, trait='extra'):
    if normalize:
        output_fp = os.path.join('result', 'feature', 'all_freq_pat_support%d_norm.csv' % support)
        input_dir = os.path.join('result', 'feature', 'freq_pat', 'normalized', 'support%d' % support)
    else:
        output_fp = os.path.join('result', 'feature', 'all_freq_pat_support%d.csv' % support)
        input_dir = os.path.join('result', 'feature', 'freq_pat', 'support%d' % support)
    #input_dir = r'result\feature\freq_pat_select\support%s\%s' % (support, trait)
    
    labels = ['uid']
    id_y = get_trait_scores() 
    ids = sorted(id_y.keys())
    all_features = {id:[] for id in ids}
    for filename in os.listdir(input_dir):
        if not '.csv' in filename:
            continue
        feature = filename[:-4]
        #print feature
        labels.append(feature)
        fp = os.path.join(input_dir, filename)
        id_feature = read_feature(fp)
        for id in all_features:
            all_features[id].extend(id_feature[id])
        #print id_all_features
    fw = open(output_fp, 'a')
    labels.append(trait)
    fw.write(','.join(labels) + '\n')  
    trait_idx = TRAITS.index(trait)
    for id in ids:
        line = [id]
        line.extend(all_features[id])
        line.append(id_y[id][trait_idx])
        fw.write(','.join(line) + '\n') 
    fw.close()
    
        
def combine_heuristic_fp(fnames,trait='extra'):       
    output_fp = os.path.join('result', 'feature', 'combined_all_%s.csv' % trait)
    input_dir = os.path.join('result', 'feature')
    labels = ['uid']
    id_y = get_trait_scores(trait)  
    ids = sorted(id_y.keys())
    all_features = {id:[] for id in ids}
    for fname in fnames:
        fr = open(os.path.join(input_dir, fname), 'rU')
        labels.extend(fr.readline().split(',')[1:-1])
        id_feature = {}
        for line in fr.readlines():
            items = line.split(',')
            id = items[0]
            features = items[1:-1]
            all_features[id].extend(features)
             
    labels.append(trait)
    fw = open(output_fp, 'a')
    fw.write(','.join(labels) + '\n')  
    for id in ids:
        line = [id]
        line.extend(all_features[id]) 
        line.append(id_y[id])
        fw.write(','.join(line) + '\n') 
    fw.close()
        
        
if __name__ == '__main__':
#     fnames = ['len_var', 'start_time_var', 'end_time_var']
#     fnames.extend(['early-late-absent', 'late_time_var'])
#     fnames.append('days-views-contributions-questions-notes-answers')
#     fnames.append('breakfast-lunch-supper-snack')
    #combine_heuristic_features(fnames)
    
    #combine_freq_patterns(40, normalize=True)
    
    combine_heuristic_fp(['all_heuristic_features_extra.csv','all_freq_pat_support40_norm.csv'], 'extra')
 
    






