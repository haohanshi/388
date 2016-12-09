class SVM:
    def __init__(self, X, y, reg):
        """ Initialize the SVM attributes and initialize the weights vector to the zero vector. 
            Attributes: 
                X (array_like) : training data intputs
                y (vector) : 1D numpy array of training data outputs
                reg (float) : regularizer parameter
                theta : 1D numpy array of weights
        """
        self.X = X
        self.y = y
        self.reg = reg
        self.theta = np.zeros(X.shape[1])

    def objective(self, X, y):
        """ Calculate the objective value of the SVM. When given the training data (self.X, self.y), this is the 
            actual objective being optimized. 
            Args:
                X (array_like) : array of examples, where each row is an example
                y (array_like) : array of outputs for the training examples
            Output:
                (float) : objective value of the SVM when calculated on X,y
        """
        # objective is hinge loss function
        y = sp.diags(y)
        X = sp.csr_matrix(X)
        Xy = y.dot(X)
        hinge_loss = np.sum(np.maximum(1 - Xy.dot(self.theta), 0))
        regularization = self.reg/2.0 * (np.linalg.norm(self.theta))**2
        return hinge_loss + regularization

    def gradient(self):
        """ Calculate the gradient of the objective value on the training examples. 
            Output:
                (vector) : 1D numpy array containing the gradient
        """
        X = sp.csr_matrix(self.X)
        y = sp.diags(self.y)
        Xy = y.dot(X)
        return -Xy.T.dot(Xy.dot(self.theta) <= 1) + self.reg*self.theta

    def train(self, niters=100, learning_rate=1, verbose=False):
        """ Train the support vector machine with the given parameters. 
            Args: 
                niters (int) : the number of iterations of gradient descent to run
                learning_rate (float) : the learning rate (or step size) to use when training
                verbose (bool) : an optional parameter that you can use to print useful information (like objective value)
        """
        for i in range(niters):
            if (verbose):
                print self.objective(self.X, self.y)
            self.theta -= learning_rate*(self.gradient())

    def predict(self, X):
        """ Predict the class of each label in X. 
            Args: 
                X (array_like) : array of examples, where each row is an example
            Output:
                (vector) : 1D numpy array containing predicted labels
        """
        res = X.dot(self.theta)
        res[res == 0] = 0.1 # take care of edge case where hypothesis is 0
        return np.sign(res)
