from svm import SVM
import numpy as np

class ModelSelector:
    """ A class that performs model selection. 
        Attributes:
            blocks (list) : list of lists of indices of each block used for k-fold cross validation, e.g. blocks[i] 
            gives the indices of the examples in the ith block 
            test_block (list) : list of indices of the test block that used only for reporting results
            
    """
    def __init__(self, X, y, P, k, niters):
        """ Initialize the model selection with data and split into train/valid/test sets. Split the permutation into blocks 
            and save the block indices as an attribute to the model. 
            Args:
                X (array_like) : array of features for the datapoints
                y (vector) : 1D numpy array containing the output labels for the datapoints
                P (vector) : 1D numpy array containing a random permutation of the datapoints
                k (int) : number of folds
                niters (int) : number of iterations to train for
        """
        self.X = X
        self.y = y
        self.k = k
        
        self.chunk_size = (y.shape[0] + k) / (k+1)
        chunks = np.array_split(P, self.chunk_size)
        self.blocks = np.split(P[:k * self.chunk_size], k)
        self.test_block = P[k * self.chunk_size:]
        
        self.niters = niters

    def cross_validation(self, lr, reg):
        """ Given the permutation P in the class, evaluate the SVM using k-fold cross validation for the given parameters 
            over the permutation
            Args: 
                lr (float) : learning rate
                reg (float) : regularizer parameter
            Output: 
                (float) : the cross validated error rate
        """
        err = 0.0
        total = float(self.k * self.chunk_size)
        
        for i, block in enumerate(self.blocks):
            # exclude current block in cross validation
            blocks = np.array(self.blocks[:i] + self.blocks[i+1:])

            training_set = blocks.flatten()
            svm = SVM(self.X[training_set], self.y[training_set], reg)
            svm.train(self.niters, lr)
            
            validation_set = block
            prediction = svm.predict(self.X[validation_set]).astype(int)
            actual = self.y[validation_set]
            
            err += (np.sign(prediction) != np.sign(actual)).sum()
        
        return err / total
    
    def grid_search(self, lrs, regs):
        """ Given two lists of parameters for learning rate and regularization parameter, perform a grid search using
            k-wise cross validation to select the best parameters. 
            Args:  
                lrs (list) : list of potential learning rates
                regs (list) : list of potential regularizers
            Output: 
                (lr, reg) : 2-tuple of the best found parameters
        """
        best = None
        l = r = 0
        
        for lr in lrs:
            for reg in regs:
                err = self.cross_validation(lr, reg)
                if best is None or err < best:
                    l, r = lr, reg
                    best = err
        return l, r
    
    def test(self, lr, reg):
        """ Given parameters, calculate the error rate of the test data given the rest of the data. 
            Args: 
                lr (float) : learning rate
                reg (float) : regularizer parameter
            Output: 
                (err, svm) : tuple of the error rate of the SVM on the test data and the learned model
        """
        training_set = np.array(self.blocks).flatten()
        svm = SVM(self.X[training_set], self.y[training_set], reg)
        svm.train(self.niters, lr)
        
        test_set = self.test_block
        prediction = svm.predict(self.X[test_set])
        actual = self.y[test_set]
        
        err = (prediction != actual).sum()
        total = float(len(test_set))
        
        return err / total, svm
