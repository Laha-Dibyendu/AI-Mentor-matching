import json
import numpy as np
import pandas as pd
import _pickle as pickle
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report, silhouette_score, davies_bouldin_score

## Loading in the original unclustered DF
with open("profiles33.pkl", 'rb') as fp:
    raw_df = pickle.load(fp)

# Function to make the clusters and returning the Mentor. Taking the existing pool of data as raw_df and the new input as new_profile 
class In22labs_Mentor_mentee:

    def predict_mentor( new_profile, raw_df = raw_df):
        # Giving the new profile as the last index +1 of the existing data
        new_profile.index = [raw_df.index[-1] + 1]
        # Appending the new data
        # new_cluster = raw_df.append(new_profile)
        new_cluster = pd.concat([raw_df,new_profile])
        # Initializing the TfidfVectorizer. converting text data into a matrix of TF-IDF (Term Frequency-Inverse Document Frequency) features. 
        # The stop_words='english' parameter is used to specify that common English stop words (e.g. "a", "an", "the", "and", etc.) should be removed from the input text before calculating the TF-IDF values.
        vectorizer = TfidfVectorizer(stop_words='english')
        df = new_cluster['About']
        x = vectorizer.fit_transform(df)
        # Creating a new DF that contains the vectorized words
        df_wrds = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names_out())
        # Concating the words DF with the original DF
        new_df = pd.concat([df, df_wrds], axis=1)
        # Dropping the About because it is no longer needed in place of vectorization. Since it is already transformed to many columns using tfidf
        new_df.drop('About', axis=1, inplace=True)
        # Instantiating PCA. Which choses the Principal components which is actually helping to make the clusters
        pca = PCA()
        # Fitting and Transforming the DF
        df_pca = pca.fit_transform(new_df)
        # Instantiating HAC. 
        # AgglomerativeClustering is a clustering algorithm from the scikit-learn library that is used to group similar data points 
        # into clusters based on their pairwise distances
        hac = AgglomerativeClustering(n_clusters=19)
        # Fitting
        hac.fit(df_pca)
        # Getting cluster assignments
        cluster_assignments = hac.labels_
        # Unscaling the categories then replacing the scaled values
        df = new_cluster
        # Assigning the clusters to each profile
        df['Cluster #'] = cluster_assignments
        ## Finding the Exact Cluster for our New Profile
        # Getting the Cluster # for the new profile
        profile_cluster = df.loc[new_profile.index]['Cluster #'].values[0]
        # Using the Cluster # to narrow down the DF
        profile_df = df[df['Cluster #'] ==
                        profile_cluster].drop('Cluster #', axis=1)
        ## Vectorizing
        # Fitting the vectorizer to the About
        cluster_x = vectorizer.fit_transform(profile_df['About'])
        # Creating a new DF that contains the vectorized words
        cluster_v = pd.DataFrame(cluster_x.toarray(), index=profile_df.index, columns=vectorizer.get_feature_names_out())
        # Joining the Vectorized DF to the previous DF
        profile_df = profile_df.join(cluster_v).drop(
            columns=['Name', 'About'], axis=1)
        ## Correlation
        # Trasnposing the DF so that we are correlating with the index(users) and finding the correlation
        corr = profile_df.T.corr()
        # Finding the Top 10 similar or correlated users to the new user
        user_n = new_profile.index[0]
        # Creating a DF with the Top 10 most similar profiles
        top_10_sim = corr[[user_n]].sort_values(
            by=[user_n], axis=0, ascending=False)[1:11]
        # Displaying the Top 10
        json_data = raw_df.loc[top_10_sim.index]
        pred = json_data.to_json(orient='records')
        return pred
    