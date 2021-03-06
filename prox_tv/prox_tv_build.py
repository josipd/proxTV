import os
import os.path

from cffi import FFI


ffi = FFI()
ffi.cdef("""
    typedef struct {
        ...;
    } Workspace;

    // Condat's implementatino.
    void TV1D_denoise(double* input, double* output, const int width,
                      const double lambda);
    // Ryan's implementation of Johnson's algorithm
    void dp(int n, double *y, double lam, double *beta);

    /* TV-L1 solvers */

    int tautString_TV1(double *y, double lambda, double *x,int n);
    int PN_TV1(double *y, double lambda, double *x, double *info, int n,
               double sigma, Workspace *ws);

    /* Weighted TV-L1 solvers */
    int PN_TV1_Weighted(double* Y, double* W, double* X, double* info, int n,
                        double sigma, Workspace* ws);
    int tautString_TV1_Weighted(double *y, double* lambda, double *x, int n);

    /* TV-L2 solvers */
    int more_TV2(double *y,double lambda, double *x, double *info, int n);
    int PG_TV2(double *y, double lambda, double *x,double *info, int n);
    int morePG_TV2(double *y, double lambda, double *x, double *info, int n,
                   Workspace *ws);

    /* Weighted TV-L2 solvers */
    int DR2L1W_TV(size_t M, size_t N, double* unary, double*W1, double*W2,
                  double *s, int nThreads, int maxit, double* info);


    /* 2-dimensional TV solvers */
    int PD2_TV(double *y, double *lambdas, double *norms, double *dims,
               double *x, double *info, int *ns, int nds, int npen, int ncores,
               int maxIters);
    int DR2_TV(size_t M, size_t N, double*unary, double W1, double W2,
               double norm1, double norm2, double*s, int nThreads, int maxit,
               double* info);
    int CondatChambollePock2_TV(size_t M, size_t N, double*Y, double lambda,
                                double*X, short alg, int maxit, double* info);
    int Yang2_TV(size_t M, size_t N, double*Y, double lambda, double*X,
                 int maxit, double* info);

    /* General-dimension TV solvers */
    int PD_TV(double *y, double *lambdas, double *norms, double *dims,
                double *x, double *info, int *ns, int nds, int npen,
                int ncores, int maxIters);

    /* TV-Lp solvers */
    int GP_TVp(double *y, double lambda, double *x, double *info, int n,
               double p, Workspace *ws);
    int OGP_TVp(double *y, double lambda, double *x, double *info, int n,
                double p, Workspace *ws);
    int FISTA_TVp(double *y, double lambda, double *x, double *info, int n,
                  double p, Workspace *ws);
    int FW_TVp(double *y, double lambda, double *x, double *info, int n,
               double p, Workspace *ws);
    int GPFW_TVp(double *y, double lambda, double *x, double *info, int n,
                 double p, Workspace *ws);
""")

sources = [os.path.join('src', fname) for fname in (
    'condat_fast_tv.cpp', 'johnsonRyanTV.cpp', 'LPopt.cpp', 'TV2Dopt.cpp',
    'TV2DWopt.cpp', 'TVgenopt.cpp', 'TVL1opt.cpp', 'TVL1Wopt.cpp',
    'TVL2opt.cpp', 'TVLPopt.cpp', 'TVNDopt.cpp', 'utils.cpp'
)]

ffi.set_source(
    '_prox_tv',
    """
    typedef struct {
        /* Size of memory vectors */
        int n;
        /* Generic memory which can be used by 1D algorithms */
        double **d;
        int maxd, nd;
        int **i;
        int maxi, ni;
        /* Memory for inputs and outputs */
        double *in,*out;
        /* Warm restart variables */
        short warm;
        double *warmDual;
        double warmLambda;
    } Workspace;
    """,
    sources=sources,
    define_macros=[('NOMATLAB', 1)],
    extra_compile_args=['-fopenmp'],
    extra_link_args=['-fopenmp'],
    libraries=['lapack']
)


if __name__ == '__main__':
    ffi.compile()
