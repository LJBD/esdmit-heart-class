from anderson_darling_test import AndersonDarlingTest
from scipy.cluster.vq import kmeans2
import numpy
import logging
from matplotlib import pyplot


class GMeans(object):
    def __init__(self, log_level='INFO'):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        self.logger.addHandler(ch)
        # self.dummy_data = QRSData()

    def cluster_data(self, qrs_complexes, max_k=50):
        self.logger.debug('In clusterData')
        self.qrs_data = self.qrs_conversion(qrs_complexes)

        ########################################
        # Start the algorithm
        ########################################
        initial_centroid = calculate_mean(self.qrs_data)
        print('INITIAL CENTROID: ', initial_centroid)
        k = 1
        # minit='matrix' daje to, ze moge podac macierz poczatkowych centroidow jako k
        qrs_centroids, labels_for_data = kmeans2(self.qrs_data, k=numpy.array([initial_centroid]), minit='matrix', iter=100)
        # :TODO: Check how kmeans2 beahaves and what input data it requires.
        self.logger.debug('First k-means resulted in centroids: %s' % qrs_centroids)

        self.labels_dict = {}
        for i, centroid_number in enumerate(labels_for_data):
            self.labels_dict[i] = centroid_number

        while k < max_k:
            kept_centroids = []
            for centroid_index, centroid in enumerate(qrs_centroids):
                data_for_centroid = self.get_data_for_centroid(centroid_index)
                test_outcome, new_centroids, new_labels_for_data = self.run_test(centroid, data_for_centroid)
                if test_outcome:
                    kept_centroids.append(centroid)
                else:
                    for item in new_centroids:
                        kept_centroids.append(item)
                    for index in data_for_centroid:
                        index = new_labels_for_data
                    # :TODO: Add else, in which I will update the labels_for_centroid with the two new centros' indices!

            if numpy.array(kept_centroids).all() == qrs_centroids.all():
                break
        # :TODO: Finish this method!

        return qrs_centroids

    def anderson_darling_test(self, data, alpha=0.0001):
        self.logger.debug("In anderson_darling_test")
        return AndersonDarlingTest(data, alpha)

    def run_test(self, centroid, data_for_centroid):
        self.logger.debug("In run_test")
        child_centroids = self.get_child_centroids(centroid, data_for_centroid)
        real_data = self.get_real_data_from_indices(data_for_centroid)
        new_centroids, labels_for_data = kmeans2(real_data, k=child_centroids, iter=100, minit='matrix')
        if len(new_centroids) == 2:
            v = [new_centroids[0][i] - new_centroids[1][i] for i in range(len(new_centroids[0]))]
            projected_data = self.project_data_on_v(data_for_centroid, v)
            test_outcome = self.anderson_darling_test(projected_data)
            return test_outcome, new_centroids, labels_for_data
        else:
            raise ValueError('Unexpected number of centroids.')

    def project_data_on_v(self, data_for_centroid, v):
        self.logger.debug('In project_data_on_v')
        projected_data = []
        norm_of_v = numpy.linalg.norm(v)
        real_data = self.get_real_data_from_indices(data_for_centroid)
        for data_vector in real_data:
            dot_product = numpy.dot(v, data_vector)
            projected_data.append(dot_product/norm_of_v)
        return projected_data

    def get_child_centroids(self, centroid, data_for_centroid):
        self.logger.debug("In get_child_centroids")
        real_data = self.get_real_data_from_indices(data_for_centroid)
        mean = calculate_mean(real_data)
        child_centroid_1 = [centroid[i] - mean[i]/100.0 for i in range(len(centroid))]
        child_centroid_2 = [centroid[i] + mean[i]/100.0 for i in range(len(centroid))]
        return numpy.array([child_centroid_1, child_centroid_2])

    def get_real_data_from_indices(self, dict_of_indices):
        self.logger.debug("In get_real_data_from_indices")
        return numpy.array([self.qrs_data[i] for i in dict_of_indices.keys()])

    def qrs_conversion(self, qrs_complexes):
        # Ta metoda w tym momencie nie ma zadnego sensu
        # :TODO: This method might be used to prepare data for the kmeans implementation that we'll use.
        self.logger.debug('In qrs_conversion')
        return qrs_complexes

    def get_data_for_centroid(self, centroid_index):
        self.logger.debug("In get_data_for_centroid")
        data_for_centroid = {}
        for key in self.labels_dict.keys():
            if self.labels_dict[key] == centroid_index:
                data_for_centroid[key] = centroid_index
        return data_for_centroid

    # def get_normal_distribution(self, n):
    #     """
    #     This method is be used to determine a value of a multidimensional normal probability density function.
    #     :param n: required dimension of the PDF
    #     """
    #     self.normal_var = multivariate_normal(mean=[0, 0], cov=[[1, 0], [0, 1]])
    #     self.normal_var.pdf([1, 0])


def calculate_mean(input_list):
    mean = []
    for i in range(len(input_list[0])):
        vector_for_one_coordinate = [vector[i] for vector in input_list]
        mean.append(sum(vector_for_one_coordinate)/float(len(vector_for_one_coordinate)))
    return mean


def main():
    # mean = [4.56, 5.234]
    # cov = [[1, 0],
    #        [2, 5]]
    # data = numpy.random.multivariate_normal(mean=mean, cov=cov, size=(50, 1))
    # data generation
    data = numpy.vstack((numpy.random.rand(150, 2) + numpy.array([.5, .5]),
                         numpy.random.rand(150, 2) + numpy.array([1, 1]),
                         numpy.random.rand(150, 2)))
    x = [i[0] for i in data]
    y = [i[1] for i in data]

    pyplot.plot(x, y, 'ro')
    pyplot.show()
    g_means = GMeans(log_level='DEBUG')
    g_means.cluster_data(data, max_k=10)


if __name__ == '__main__':
    main()
