
import static java.lang.Math.abs;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.Vector;


class Vertex {
    int x;
    int y;
    Vertex(int _x, int _y) {     
        x = _x;
        y = _y;
    }

    String desc() {
        return String.format("%d,%d", x,y);
    }
};

class Rect {
    Vertex first;
    Vertex second;

    Rect(Vertex _a, Vertex _b) {
        first = _a;
        second = _b;
    }

    String desc() {
        return String.format("%s - %s", first.desc(), second.desc());
    }

};

public class Answer {
    public static void main(String[] args) {
        Vector<Vertex> vertices = new Vector<>();
        File file = new File(args[0]);
        try {
        Scanner sc = new Scanner(file);
        sc.useDelimiter("[,\n]");
        while(sc.hasNext()){
            int x = sc.nextInt();
            int y = sc.nextInt();
            sc.nextLine();
            vertices.add(new Vertex(x,y));
        }

        } catch(FileNotFoundException fnfe) {
            System.out.println("not found");
        }

        // Calculate largest 
        Vector<Rect> combinations = new Vector<Rect>();
        int len = vertices.size();
        for(int i = 0; i < len - 1; i++) {
            for(int j = i + 1; j < len; j++) {
                combinations.add(new Rect(vertices.get(i), vertices.get(j)));
            }
        }

        long maxA = 0;
        for(Rect rect: combinations) {
            long dx = Math.abs(rect.first.x - rect.second.x) + 1;
            long dy = Math.abs(rect.first.y - rect.second.y) + 1;
            long A = dx * dy;
            maxA = Math.max(A, maxA);
        }
        System.out.println(maxA);
        }
}

