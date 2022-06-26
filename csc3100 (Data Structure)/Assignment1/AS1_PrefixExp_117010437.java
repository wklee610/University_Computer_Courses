import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class Test {

    private static long m = 1000000007;

    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(in.readLine());
        String[] strs = new String[n];
        for (int i = 0; i < n; ++i) {
            strs[i] = in.readLine();
        }
        System.out.println(prefixExpression(strs));

    }

    public static String prefixExpression(String[] str) {
        Stack<Long> stock = new Stack<>();
        //+ - *
        try {
            for (int i = str.length - 1; i >= 0; i--) {
                switch (str[i]) {
                    case "+":
                        stock.push((stock.pop() + stock.pop()) % m);
                        break;
                    case "-":
                        stock.push((stock.pop() - stock.pop()) % m);
                        break;
                    case "*":
                        stock.push((stock.pop() * stock.pop()) % m);
                        break;
                    default:
                        stock.push(Long.parseLong(str[i]) % m);
                        break;
                }
            }
        } catch (Exception e) {
            return "Invalid";
        }
        return stock.size() != 1 ? "Invalid" : stock.pop().toString();
    }

}
