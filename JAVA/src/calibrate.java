import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;


public class calibrate {

    public static void main(String args[]) throws IOException {

        char[][] board = new char[26][26];
        char[] row = new char[]{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '1', '2', '3', '4', '5'};


            for(int i = 0; i < 26; i++) {
                char tmp = row[row.length-1];
                for(int j = row.length-1; j >= 0; j--) {
                    row[j] = j == 0 ? tmp : row[(j-1+row.length)%row.length];
                }

                for(int k=0;k<26;k++){
                    board[i][k] = row[k];
                }
            }

        homework hw = new homework();
        long start_time = System.currentTimeMillis();
        int number_of_nodes = hw.used_for_calibrate(board, 26, 3);
        long end_time = System.currentTimeMillis();
        long rate = (number_of_nodes*1000)/(end_time-start_time);

        FileWriter fw = new FileWriter("calibration.txt");
        BufferedWriter bw = new BufferedWriter(fw);
        bw.write(rate+"");
        bw.close();
        fw.close();

    }
    public static String printBoard(char[][] board, int board_size){
        String output = "";
        for(int i=0;i<board_size;i++){
            String row = "";
            for(int j=0;j<board_size;j++){
                row += board[i][j];
                System.out.print(board[i][j]);
            }
            output += row+"\n";
            System.out.println();
        }

        return output;
    }

}
