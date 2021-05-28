import Voronoi as vor
import time


def main():
    start_time = time.time()
    vor.generate_voronoi_diagram(300, 300, 10, 0.00005, 'hex', 100)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
