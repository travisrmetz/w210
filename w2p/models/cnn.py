class CNN_Model(Keras_Model):
    """
    """

    def __init__(self, output_dim=1, sequence_length=10,
                 nb_blocks=1,filters=8, kernel_size=5, activation = 'relu',
                 pooling='max', pool_strides = 2, pool_size = 5,
                 conv_dropout=0.2, fc_dropout = 0.5, dense_units = 64, batch_norm = True):
        """

        Args:
            output_dim: Output Dimensionality
            sequence_length: Length of the input sequences
            nb_blocks: Number of convolutional blocks
            filters: Number of filters in the convolutional layers
            kernel_size: Size of the kernel to use in convolutional layers
            activation: Activation function
            pooling: Type of pooling (Max or Average)
            pool_strides: Pooling strides
            pool_size: Pooling window size
            conv_dropout: Convolutional layer dropout
            fc_dropout: Fully Connected layer dropout
            dense_units: Number of hidden units in fully connected layers
            batch_norm: Boolean flag specifying whether to use batch normalisation layers
        """

        print('Initialising CNN Model... \n')

        Keras_Model.__init__(self)


        self.output_dim = output_dim
        self.sequence_length = sequence_length
        self.nb_blocks = nb_blocks
        self.filters = filters
        self.kernel_size = kernel_size
        self.activation = activation

        self.pooling = pooling
        self.conv_dropout = conv_dropout
        self.fc_dropout = fc_dropout
        self.dense_units = dense_units
        self.batch_norm = batch_norm

        self.pooling_strides = pool_strides
        self.pooling_size = pool_size

    def Build(self):
        """
        Builds the topology of the network
        """

        print('Building CNN... \n' )
        print('Filters: ', self.filters)
        print('Kernel Size: ', self.kernel_size)
        print('Number of blocks: ', self.nb_blocks)
        print('Pooling type:', self.pooling)
        print('Pooling Strides:', self.pooling_strides)
        print('Pooling Length:', self.pooling_size)

        print('Conv Dropout: ', self.conv_dropout)
        print('FC Dropout: ', self.fc_dropout)
        print('Dense Units: ', self.dense_units)
        print('Activation:', self.activation)
        print('Batch Normalisation:', self.batch_norm)
        print('\n')

        self.AddInputBlock()

        for i in range(self.nb_blocks):
            self.AddCNNBlock()

        self.AddOutputBlock()

    def AddInputBlock(self):
        """

        """

        self.model.add(Conv1D(filters=self.filters, kernel_size=self.kernel_size, input_shape=(self.sequence_length, self.output_dim)))

        # Batch Norm Layer
        if (self.batch_norm):
            self.model.add(BatchNormalization())

        # Pooling Layer
        if (self.pooling == 'max'):
            self.model.add(MaxPool1D(pool_size=self.pooling_size,strides=self.pooling_strides))
        elif (self.pooling == 'average'):
            self.model.add(AveragePooling1D(pool_size=self.pooling_size, strides=self.pooling_strides))

        # Dropout layer
        if (self.conv_dropout is not None):
            self.model.add(Dropout(self.conv_dropout))

        # Activation Layer
        if (self.activation == 'prelu'):
            self.model.add(PReLU())
        else:
            self.model.add(Activation(self.activation))


    def AddCNNBlock(self):
        """

        """

        # Convolution Layer
        self.model.add(Conv1D(filters=self.filters, kernel_size=self.kernel_size))


        # Batch Norm Layer
        if (self.batch_norm):
            self.model.add(BatchNormalization())


        # Pooling Layer
        if (self.pooling == 'max'):
            self.model.add(MaxPool1D(pool_size=self.pooling_size,strides=self.pooling_strides))
        elif (self.pooling == 'average'):
            self.model.add(AveragePooling1D(pool_size=self.pooling_size, strides=self.pooling_strides))

        # Dropout layer
        if (self.conv_dropout is not None):
            self.model.add(Dropout(self.conv_dropout))

        # Activation Layer
        if (self.activation == 'prelu'):
            self.model.add(PReLU())
        else:
            self.model.add(Activation(self.activation))


    def AddOutputBlock(self):
        """

        """

        self.model.add(Flatten())

        self.model.add(Dense(self.dense_units))

        # Dropout layer
        if self.fc_dropout is not None:
            self.model.add(Dropout(self.fc_dropout))

        # Activation Layer
        if (self.activation == 'prelu'):
            self.model.add(PReLU())
        else:
            self.model.add(Activation(self.activation))


        self.model.add(Dense(int(self.dense_units)))

        # Activation Layer
        if (self.activation == 'prelu'):
            self.model.add(PReLU())
        else:
            self.model.add(Activation(self.activation))

        if self.fc_dropout is not None:
            self.model.add(Dropout(self.fc_dropout))

        self.model.add(Dense(int(self.dense_units)))

        # Activation Layer
        if (self.activation == 'prelu'):
            self.model.add(PReLU())
        else:
            self.model.add(Activation(self.activation))

        if self.fc_dropout is not None:
            self.model.add(Dropout(self.fc_dropout))

        self.model.add(Dense(int(self.dense_units)))

        # Activation Layer
        if (self.activation == 'prelu'):
            self.model.add(PReLU())
        else:
            self.model.add(Activation(self.activation))


        self.model.add(Dense(1, activation='sigmoid'))

    def SetSequenceLength(self, seq_length):
        """

        Args:
            seq_length:
        """
        self.sequence_length = seq_length

    def SetOutputDimension(self, dim):
        """

        Args:
            dim:
        """
        self.output_dim = dim

    def SaveCNNModel(self, name, config=False, weights=False):
        """

        Args:
            name:
            config:
            weights:
        """

        root = 'models/'

        # Save model with weights and training configuration
        if (weights):
            model_json = self.model.to_json()
            with open(root + name + '.json', "w") as json_file:
                json_file.write(model_json)

            # Serialise weights
            self.model.save_weights(root + name + '.h5')

            if(config):
                with open(root + 'configs/' + name + '.json', 'w') as fp:
                    json.dump(config, fp)

        # Save configuration for rebuilding model
        else:
            dict = {}

            dict['nb_blocks'] = self.nb_blocks
            dict['filters'] = self.filters

            dict['kernel_size'] = self.kernel_size
            dict['activation'] = self.activation

            dict['pooling'] = self.pooling
            dict['pooling_strides'] = self.pooling_strides
            dict['pooling_size'] = self.pooling_size

            dict['conv_dropout'] = self.conv_dropout
            dict['fc_dropout'] = self.fc_dropout
            dict['fc_units'] = self.dense_units
            dict['batch_norm'] = self.batch_norm

            with open(root + 'configs/' + name + '.json', 'w') as fp:
                json.dump(dict, fp)



        print('Saved model to disk.')

    def LoadCNNConfiguration(self, config):
        """

        Args:
            config:
        """

        self.nb_blocks = config['nb_blocks']
        self.filters = config['filters']
        self.kernel_size = config['kernel_size']
        self.activation = config['activation']

        self.pooling = config['pooling']
        self.pooling_strides = config['pooling_strides']
        self.pooling_size = config['pooling_size']

        self.conv_dropout = config['conv_dropout']
        self.fc_dropout = config['fc_dropout']
        self.dense_units = config['fc_units']
        self.batch_norm = config['batch_norm']


        self.Build()
        self.Compile(loss='binary_crossentropy',
                    optimizer=SGD(lr=0.001 * config['lr_rate_mult'], momentum=config['momentum'], decay=0.0001,
                                  nesterov=True), metrics=['accuracy'])

        print('Loaded and compiled Keras model succesfully. \n')

    def LoadConfigurationFromFile(self, config_name):
        """

        Args:
            config_name:
        """

        root = 'models/configs/'

        # Load json configuration
        json_file = open(root + config_name + '.json', 'r')
        config_str = json_file.read()
        config = json.loads(config_str)
        json_file.close()

        self.nb_blocks = config['nb_blocks']
        self.filters = config['filters']
        self.kernel_size = config['kernel_size']
        self.activation = config['activation']

        self.pooling = config['pooling']
        self.pooling_strides = config['pooling_strides']
        self.pooling_size = config['pooling_size']

        self.conv_dropout = config['conv_dropout']
        self.fc_dropout = config['fc_dropout']
        self.dense_units = config['fc_units']
        self.batch_norm = config['batch_norm']

        #self.Build()
        #self.Compile(loss='binary_crossentropy',
        #             optimizer=SGD(lr=0.001 * config['lr_rate_mult'], momentum=config['momentum'], decay=0.0001,
        #                           nesterov=True), metrics=['accuracy'])

        #print('Loaded and compiled Keras model succesfully. \n')

