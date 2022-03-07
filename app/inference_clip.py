import os
import torch
import clip
import numpy as np
import pandas as pd
import pyarrow.feather as feather
from PIL import Image
from urllib import request
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms
import torchvision, torch
from sklearn.linear_model import LogisticRegression
import sklearn
from sklearn import metrics
from sklearn.metrics import precision_recall_fscore_support
from create_df import create_dataframe, get_mapping
# from transformers import CLIPProcessor, CLIPModel



def get_features(dataset,model,device, BATCH_SIZE=100):
    all_features = []
    all_labels = []

    with torch.no_grad():
        for images, labels in tqdm(DataLoader(dataset, batch_size=BATCH_SIZE)):
            features = model.encode_image(images.to(device))
            # images=images.type(model.dtype)
            # features=loaded(images.to(device))

            all_features.append(features)
            all_labels.append(labels)

    return torch.cat(all_features).cpu().numpy(), torch.cat(all_labels).cpu().numpy()



def clip_inference(enrollment_size=90,set_number=1):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    # device

    # PATH="/home/jupyter/train-CLIP-FT/lightning_logs/version_4/checkpoints/epoch=31-step=16319.ckpt"
    # PATH = "/home/jupyter/train-CLIP-FT/lightning_logs/version_4/checkpoints/epoch=31-step=4063.ckpt"
    # model = torch.load(PATH, map_location='cpu')
    print("model loaded")
    test_label_dict={}
    enrollment_label_dict={}


    metric_agg= pd.DataFrame(columns=["enrollment_batch_size","set_number","accuracy","precision","recall","fbeta_score","weighted_precision","weighted_recall","weighted_fbeta"])
    acc_df= pd.DataFrame()
    
    # dvc-manual/gtin_60/data/prep/subsets/enrollment_size_{enrollment_size}_SN_{set_number}
    enrollment_path= os.path.join("/home/jupyter",f'dvc-manual/gtin_60/data/prep/80gtin_allsubfolders/80gtin_ET/ET_size_{enrollment_size}')
    enrollment_preprocess= torchvision.datasets.ImageFolder(root=enrollment_path,transform=preprocess)
    # 'dvc-manual/gtin_60/data/prep/test'
    test_path= os.path.join("/home/jupyter",'dvc-manual/gtin_60/data/prep/80gtin_allsubfolders/splitfolders/test')
    test_preprocess= torchvision.datasets.ImageFolder(root=test_path,transform=preprocess)

    for k,v in test_preprocess.class_to_idx.items():
        test_label_dict[v]=k
    for k,v in enrollment_preprocess.class_to_idx.items():
        enrollment_label_dict[v]=k

    enrollment_features, enrollment_labels = get_features(enrollment_preprocess,model,device, 100)
    test_features, test_labels = get_features(test_preprocess,model,device, 100)

    classifier = LogisticRegression(random_state=0, C=0.316, max_iter=1000, verbose=0)
    classifier.fit(enrollment_features, enrollment_labels)



    predictions = classifier.predict(test_features)
    true_labels=test_labels.copy()

    for idx,val in enumerate(test_labels):
        true_labels[idx]=test_label_dict[val]

    for idx,val in enumerate(predictions):
        predictions[idx]=enrollment_label_dict[val]

    acc= metrics.accuracy_score(np.array(true_labels),np.array(predictions))
    report=sklearn.metrics.classification_report(np.array(true_labels),np.array(predictions))
    prec, rec,fscore,supp=precision_recall_fscore_support(np.array(true_labels),np.array(predictions), average='macro')
    w_prec, w_rec,w_fscore,w_supp=precision_recall_fscore_support(np.array(true_labels),np.array(predictions), average='weighted')

    row={"enrollment_batch_size": enrollment_size,
             "set_number": set_number,
             "accuracy": acc,
             "precision":prec,
             "recall": rec,
             "fbeta_score": fscore,
             "weighted_precision": w_prec,
             "weighted_recall": w_rec,
             "weighted_fbeta": w_fscore
            }
    metric_agg=metric_agg.append(row,ignore_index=True)
    print(f"Enrollment size = {enrollment_size}")
    print("Accuracy= ", acc)
        
    #################################################
    # Add predictions and true labels to dataframe #
    #################################################
    label_col= "name"
    test_path= os.path.join('/home/jupyter/dvc-manual/gtin_60/data/prep/80gtin_allsubfolders/splitfolders/test')
    test_df=create_dataframe(test_path, label_col)

    test_df_full=pd.concat([test_df,pd.Series(true_labels,name="true_label_gtin",),pd.Series(predictions,name="predicted_label_gtin")],axis=1)
    test_df_full["true_label_gtin"] = test_df_full["true_label_gtin"].apply(lambda x: str(x).zfill(14))
    test_df_full["predicted_label_gtin"] = test_df_full["predicted_label_gtin"].apply(lambda x: str(x).zfill(14))
    enrollment_path= os.path.join(f'/home/jupyter/dvc-manual/gtin_60/data/prep/80gtin_allsubfolders/80gtin_ET/ET_size_{str(enrollment_size)}')
    test_df_full["predicted_gtin_enroll_folder"]=test_df_full.apply(lambda x:os.path.join(enrollment_path,x["predicted_label_gtin"]),axis=1)
    
    test_df_full["is_correct"]=test_df_full.apply(lambda x: True if x["true_label_gtin"]==x["predicted_label_gtin"] else False,axis=1)
    misclassifications=test_df_full[test_df_full["is_correct"]==False]
    gtin_mapping = get_mapping()
    misclassifications = misclassifications.merge(gtin_mapping.loc[:,["name","gtin"]].add_suffix('_predictions'), left_on=["predicted_label_gtin"], right_on=["gtin_predictions"], how="left")
    return metric_agg, misclassifications
    
if __name__=='__main__':
    enrollment_size=90
    set_num=1
    metrics,misclassifications=clip_inference(enrollment_size,set_num)
    print(metrics)
    misclassifications.to_csv(f"misclassifications_ET{enrollment_size}_SN{set_num}.csv")
    """
        ## True labels, predicted labels
        Recall, precision, accuracy, f-beta score
        Save misclassifications as a dataset to db
        Find all images where true labels <> predicted labels:
            - Predicted class label
            - True Label
            - True image oath
            - Predicted gtin folder path
            
        Provide feedback ; Store feedback
        """