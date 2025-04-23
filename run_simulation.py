import sys
from simulation import Simulation

if __name__ == '__main__':
    if len(sys.argv) > 1:
        param = sys.argv[1]
    else:
        param = "mặc định"

    print(f"Khởi chạy mô phỏng với tham số: {param}")
    sim = Simulation(param)
    sim.run()