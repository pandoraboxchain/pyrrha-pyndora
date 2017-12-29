import keras
import h5py
import numpy as np

from ipfs.connector import IPFSConnector

def load(arch: str, weights: str, data: str, files_dir: str):
    print('Loading kernel architecture...')
    with open(arch, "r") as json_file:
        json_model = json_file.read()
    model = keras.models.model_from_json(json_model)

    print('Loading kernel weights...')
    model.load_weights(weights)
    h5f = h5py.File(data, 'r')
    # FIX: Magic number for dataset name inside HDF5 file!
    h5ds = h5f['dataset']
    dataset = np.ndarray(shape=h5ds.shape)
    h5ds.read_direct(dest=dataset)
    return {
        'model': model,
        'dataset': dataset,
    }

def load_and_run(arch: str, weights: str, data: str, files_dir: str):

    print('Loading kernel architecture...')
    with open(arch, "r") as json_file:
        json_model = json_file.read()
    model = keras.models.model_from_json(json_model)

    print('Loading kernel weights...')
    model.load_weights(weights)
    h5f = h5py.File(data, 'r')
    # FIX: Magic number for dataset name inside HDF5 file!
    h5ds = h5f['dataset']
    dataset = np.ndarray(shape=h5ds.shape)
    h5ds.read_direct(dest=dataset)

    print('Cogniting...')
    out = model.predict(dataset)
    print('Cognition completed successfully:')
    h5w = h5py.File('out.hdf5', 'w')
    h5w.create_dataset('dataset', data=out)
