import numpy as np
from Transformation import *
from Point_cloud import Point_cloud
from Generalized_ICP import *
from utils.ply import write_ply

if __name__ == '__main__':

    if False: # Script for gradient check
        theta = np.array([2,-1,0.5])
        print(rot_mat(theta))

        grm = grad_rot_mat(theta)

        epsilon  = 1e-8
        for i in range(3):
            print("check gradient "+str(i))
            epsilon_vec = np.zeros(3)
            epsilon_vec[i] = epsilon
            print(grm[i])
            print((rot_mat(theta + epsilon_vec) - rot_mat(theta - epsilon_vec))/2/epsilon)


    if True: # Script to test on several simulations the methods on several thresholds
        # Cloud paths
        bunny_path = './data/bunny_original.ply'

        total = Point_cloud()
        total.init_from_ply(bunny_path)

        data = Point_cloud()
        ref = Point_cloud()

        n_iter = 50
        thresholds = [0.07,0.08,0.09,0.1,0.11,0.12]
        methods = ["point2point","point2plane","plane2plane"]

        # Initailization of the reference cloud
        ref.init_from_points(total.points[5000:])
        last_rms = np.zeros((len(thresholds),n_iter,len(methods)))
        np.savetxt("spec_res.txt",thresholds)

        for id_t,threshold in enumerate(thresholds):
            for i in range(n_iter):
                print("Iteration {}".format(i+1))
                grad_to_deg = 3.14/180

                # random transformation
                R_0 = rot_mat(np.random.uniform(low = -15*grad_to_deg,high = 15*grad_to_deg, size = (3,)))
                T_0 = np.random.uniform(low = -0.01,high = 0.01)


                # initialization of the cloud to align
                data.init_from_points(total.points[:10000])
                data.transform(R_0,T_0)

                for id_m,method in enumerate(methods):
                    print("\t ICP with {} method".format(method))
                    R, T, rms_list = ICP(data,ref, method = method, exclusion_radius = threshold ,sampling_limit = None, verbose = False)
                    last_rms[id_t,i,id_m] = rms_list[-1]
                    np.savetxt("res_{}.csv".format(method),last_rms[:,:,id_m])
