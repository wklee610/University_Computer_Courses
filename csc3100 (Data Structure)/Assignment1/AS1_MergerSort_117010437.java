import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Test {
    public static void main(String[] args) throws IOException {
        BufferedReader in  = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(in.readLine());
        long[] list = new long[n];
        for (int i = 0; i < n; ++i) list[i] = Long.parseLong(in.readLine());
        new Solution().mergeSort(0, list.length - 1, list);
        for (Long num: list) System.out.println(num);
    }


}

class Solution {
    public void mergeSort(int left, int right, long[] list) {
        if (left >= right) return;
        int mid = (left + right) / 2;
        mergeSort(left, mid, list);
        mergeSort(mid + 1, right, list);
        merge(list, left, mid, right);

    }

    public void merge(long[] list, int left, int mid, int right) {
        int ptr1 = 0;
        int ptr2 = 0;
        int index = left;
        long[] temp_left = new long[mid - left + 1];
        long[] temp_right = new long[right - mid];
        for (int i = 0; i < mid-left + 1; i ++) {
            temp_left[i] = list[left + i];
        }
        for (int i = 0; i < right - mid; i ++) {
            temp_right[i] = list[mid + 1 + i];
        }

        while (index <= right) {
            if (ptr1 >= mid - left + 1) {
                list[index] = temp_right[ptr2];
                ptr2++;
                index++;
                continue;
            }
            if (ptr2 >= right - mid) {
                list[index] = temp_left[ptr1];
                ptr1++;
                index++;
                continue;
            }
            if (temp_left[ptr1] <= temp_right[ptr2]) {
                list[index] = temp_left[ptr1];
                ptr1++;
            } else {
                list[index] = temp_right[ptr2];
                ptr2++;
            }
            index++;
        }
    }
}
