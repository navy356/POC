#include <iostream>
#include <memory>
#include <vector>

class Service {
  public:
    Service() {
      std::cin.rdbuf()->pubsetbuf(0, 0);
      std::cin.setf(std::ios::unitbuf);
      std::cout.rdbuf()->pubsetbuf(0,0);
      std::cout.setf(std::ios::unitbuf);
    }
    void create() {vecs.push_back(std::vector<uint8_t>());}
    void push(uint8_t key, uint8_t byte) {vecs.at(key).push_back(byte);}
    void set(uint8_t key, uint8_t byte, uint32_t idx) {vecs.at(key)[idx] = byte;}
    void get(uint8_t key, uint32_t idx) {std::cout << vecs.at(key).at(idx) << std::endl;}
  private:
    std::vector<std::vector<uint8_t>> vecs;
};

int main() {
  uint8_t key, byte;
  uint32_t index, cmd;
  std::unique_ptr<Service> service = std::make_unique<Service>();
  while(true) {
    std::cout << ">> ";
    std::cin >> cmd;
    switch(cmd) {
      case 0: {
        service->create();
        break;
      }
      case 1: {
        std::cin >> key;
        std::cin >> byte;
        service->push(key, byte);
        break;
      }
      case 2: {
        std::cin >> key;
        std::cin >> index;
        std::cin >> byte;
        service->set(key, byte, index);
        break;
      }
      case 3: {
        std::cin >> key;
        std::cin >> index;
        service->get(key, index);
        break;
      }
      default: {
        exit(-1);
      }
    }
  }
  return 0;
}
