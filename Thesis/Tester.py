# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 10:41:27 2020

@author: Edoardo Vantaggiato
"""

import torch
import datetime
from sklearn.metrics import f1_score, confusion_matrix, classification_report
from time import sleep
from tqdm import tqdm

import Utils as utils
import AUC as auc

def test(model, device, test_loader, test_size, model_name, model_path=''):
    if model_path != '':
        model.load_state_dict(torch.load(model_path))
    model = model.to(device)

    model.eval()
    running_corrects = 0
    tot_labels = []
    tot_preds = []
    out = []
    print('\n[INFO] Testing started with ' + model_name + '\n')
    sleep(0.2)
    tqdm_test = tqdm(test_loader)
    classes = test_loader.dataset.classes

    for i, (inputs, labels) in enumerate(tqdm_test):
        start, end = 0, 0
        inputs = inputs.to(device)
        labels = labels.to(device)
        start = datetime.datetime.now()
        with torch.no_grad():
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
        end = datetime.datetime.now()
        elapsed = end - start
        for x in labels:
            tot_labels.append(x.item())
        for y in preds:
            tot_preds.append(y.item())
        out.extend(outputs)
        running_corrects += torch.sum(preds == labels)
        # if labels.item() == 1 and preds != labels:
        #     sample_fname, _ = test_loader.dataset.samples[i]
        #     print(sample_fname.split('\\')[-1])
        #     print('pred', preds.item(),'label', labels.item())

    sleep(0.2)
    test_acc = running_corrects.double() / test_size  # modify to run also in validation phase
    f1_test = f1_score(tot_labels, tot_preds, average='micro')
    cm = confusion_matrix(tot_labels, tot_preds)
    print("- test accuracy = {}\n- test F1-score = {}\n- Elapsed time = {} microsecond".format(test_acc, f1_test, elapsed.microseconds))
    utils.auc_score(tot_labels, tot_preds, classes)
    pr, se, sp = utils.compute_report(cm, classes)
    print('- precision = ', pr)
    print('- sensitivity = ', se)
    print('- specificity = ', sp)
    print("[INFO] Testing complete")

    return test_acc, f1_test, cm, out, tot_labels, tot_preds
