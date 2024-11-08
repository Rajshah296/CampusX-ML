from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

def pca_func(X_train, X_test, variance_needed=90, pca_params=None, random_state=None):
    
    # Ensure pca_params is a dictionary
    if pca_params is None:
        pca_params = {}

    # Scale the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Fit PCA once with max components
    pca = PCA(n_components=X_train.shape[1], random_state=random_state, **pca_params)
    X_train_transformed = pca.fit_transform(X_train)
    
    # Calculate cumulative explained variance
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_ * 100)
    
    # Find the minimum number of components needed to meet the variance threshold
    if variance_needed > cumulative_variance[-1]:
        print(f"Warning: Desired variance of {variance_needed}% cannot be reached. Using maximum components.")
        n_components_optimal = X_train.shape[1]
    else:
        n_components_optimal = np.argmax(cumulative_variance >= variance_needed) + 1
    
    # Transform X_train and X_test with the optimal number of components
    X_train_trf = X_train_transformed[:, :n_components_optimal]
    X_test_trf = pca.transform(X_test)[:, :n_components_optimal]
    
    # Create a PCA instance for reference with the optimal number of components
    pca_optimal = PCA(n_components=n_components_optimal, random_state=random_state, **pca_params)
    pca_optimal.fit(X_train)  # For documentation/reference purposes only
    
    # Return PCA model and transformed data
    return pca_optimal, X_train_trf, X_test_trf