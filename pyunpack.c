#include <Python.h>
#include "unpack.h"


#define HEADER_SIZE     0x279

static PyObject* unpack_unpack(PyObject *, PyObject *);


static PyObject*
unpack_unpack(PyObject *self, PyObject *args)
{
    FILE *fd;
    const char *filename;
    byte *buf;
    dword rep;
    PyObject *rep_id, *header, *tuple;

    if (!PyArg_ParseTuple(args, "s", &filename))
        return NULL;

    fd = fopen(filename, "rb");
    if (fd == NULL) {
        PyErr_SetString(PyExc_OSError, "Could not open replay file.");
        return NULL;
    }
    
    /* Get the replay ID (must always be 0x53526572) */
    unpack_section(fd, (byte *)&rep, sizeof(rep));
    rep_id = PyInt_FromLong(rep);

    /* Get the header.  Its size is always 0x279. */
    buf = malloc(HEADER_SIZE * sizeof(byte));
    if (buf == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate space.");
        return NULL;
    }
    unpack_section(fd, buf, sizeof(byte) * HEADER_SIZE);
    header = PyString_FromStringAndSize((char *)buf,
                                        sizeof(byte) * HEADER_SIZE);

    fclose(fd);

    tuple = PyTuple_New(2);
    PyTuple_SetItem(tuple, 0, rep_id);
    PyTuple_SetItem(tuple, 1, header);
    return tuple;
}

static PyMethodDef UnpackMethods[] = {
    {"unpack",  unpack_unpack, METH_VARARGS, "Unpack a REP file."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
init_unpack(void)
{
    (void)Py_InitModule("_unpack", UnpackMethods);
}
