#include <sstream>
#include <string>
#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

class Vertex {
    public:
     int x,y;

     Vertex(int _x, int _y) {
        x = _x;
        y = _y;
     }
};
int main(void) {
	std::ifstream input("./input.txt");
	int a,b;
	char comma;
	vector<Vertex> vertices;
	while (input >> a >> comma >> b) {
		vertices.push_back(Vertex(a,b));
	}

    // Calculate largest 
    vector<pair<Vertex,Vertex>> combinations;
    size_t len = vertices.size();
    for(int i = 0; i < len - 1; i++) {
        for(int j = i + 1; j < len; j++) {
            combinations.push_back(pair<Vertex,Vertex>(vertices[i], vertices[j]));
        }
    }

    long maxA = 0;
    for(auto rect: combinations) {
        long dx = abs(rect.first.x - rect.second.x) + 1;
        long dy = abs(rect.first.y - rect.second.y) + 1;
        long A = dx * dy;
        maxA = max(A, maxA);
    }
    cout << maxA << endl;
        
    // Now do part 2
    vector<pair<Vertex,Vertex>> edges;
    for(int i = 0; i < len - 1; i++) {
        edges.push_back(pair<Vertex,Vertex>(vertices[i], vertices[i+1]));
    }
    edges.push_back(pair<Vertex,Vertex>(vertices[len-1], vertices[0]));
    
    maxA = 0;
    // part1 = max((abs(x0-x1)+1)*(abs(y0-y1)+1) for (x0, y0), (x1, y1) in combinations(vertices,2))
    for(auto rect : combinations) {
        int x0 = rect.first.x;
        int y0 = rect.first.y;
        int x1 = rect.second.x;
        int y1 = rect.second.y;
        int min_x = min(x0,x1);
        int min_y = min(y0,y1);
        int max_x = max(x0,x1);
        int max_y = max(y0,y1);
        
        bool ok = true;
        for(auto edge: edges) {
            int v_x = edge.first.x;
            int h_y = edge.first.y;
            int min_h_x = min(edge.first.x, edge.second.x);
            int max_h_x = max(edge.first.x, edge.second.x);
            int min_v_y = min(edge.first.y, edge.second.y);
            int max_v_y = max(edge.first.y, edge.second.y);
            
            if (min_x < v_x and v_x < max_x and (max_y > min_v_y and min_y < max_v_y)) {
                ok = false;
                break;            
            }
            if (min_y < h_y and h_y < max_y and (max_x > min_h_x and min_x < max_h_x)) {
                ok = false;
                break;            
            }
        }
        if(ok) {
            long dx = abs(rect.first.x - rect.second.x) + 1;
            long dy = abs(rect.first.y - rect.second.y) + 1;
            long A = dx * dy;
            maxA = max(A, maxA);
        }

    }
    cout << maxA << endl;

    // 
	return 0;
}
