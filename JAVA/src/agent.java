
import java.io.*;
import java.util.*;

public class Submission {

    static int number_of_nodes_expanded;

    public static String printBoard(char[][] board, int board_size){
        String output = "";
        for(int i=0;i<board_size;i++){
            String row = "";
            for(int j=0;j<board_size;j++){
                row += board[i][j];
                //System.out.print(board[i][j]);
            }
            output += row+"\n";
            //System.out.println();
        }

        return output;
    }

    public static TreeMap<Integer, List<List<List<Integer>>>> possibleMoves(char[][] board, int board_size) {

        TreeMap<Integer, List<List<List<Integer>>>> possible_moves = new TreeMap<>(Collections.reverseOrder());
        int[][] visited_board = new int[board_size][board_size];

        for (int i = 0; i < board_size; i++) {

            for (int j = 0; j < board_size; j++) {

                if (visited_board[i][j] == 1 || board[i][j] == '*') {
                    continue;

                } else {

                    visited_board[i][j] = 1;
                    List<List<Integer>> move_list = playGame(board, board_size, visited_board, i, j, board[i][j]);
                    int move_len = move_list.size();

                    if (possible_moves.containsKey(move_len)) {
                        List<List<List<Integer>>> a = possible_moves.get(move_len);
                        a.add(move_list);
                        possible_moves.replace(move_len, possible_moves.get(move_len), a);
                    } else {
                        ArrayList tempList = new ArrayList<>();
                        tempList.add(move_list);
                        possible_moves.put(move_len, tempList);
                    }

                }
            }
        }

        return possible_moves;
    }

    public static List<List<Integer>> playGame(char[][] board, int board_size, int[][] visited_board, int current_row, int current_col, char current_fruit) {

        Queue queue = new LinkedList();
        queue.add(Arrays.asList(current_row,current_col));
        List<List<Integer>> fruit_list = new ArrayList<>();

        fruit_list.add(Arrays.asList(current_row,current_col));

        while (!queue.isEmpty()) {
            List<Integer> numbers = (List<Integer>) queue.remove();
            int row = numbers.get(0);
            int col = numbers.get(1);

            if (col - 1 > -1 && visited_board[row][col - 1] == 0 && board[row][col - 1] == current_fruit) {

                visited_board[row][col - 1] = 1;
                fruit_list.add(Arrays.asList(row,col - 1));
                queue.add(Arrays.asList(row,col - 1));
            }

            if (col + 1 < board_size && visited_board[row][col + 1] == 0 && board[row][col + 1] == current_fruit) {

                visited_board[row][col + 1] = 1;
                fruit_list.add(Arrays.asList(row,col + 1));
                queue.add(Arrays.asList(row,col + 1));
            }

            if (row - 1 > -1 && visited_board[row - 1][col] == 0 && board[row - 1][col] == current_fruit) {
                visited_board[row - 1][col] = 1;
                fruit_list.add(Arrays.asList(row-1,col));
                queue.add(Arrays.asList(row-1,col));
            }

            if (row + 1 < board_size && visited_board[row + 1][col] == 0 && board[row + 1][col] == current_fruit) {
                visited_board[row + 1][col] = 1;
                fruit_list.add(Arrays.asList(row+1,col));
                queue.add(Arrays.asList(row+1,col));

            }

        }

        return fruit_list;
    }

    public static void gravity1(char[][] board, int board_size, List<List<Integer>> coordinates) {


        for (int i = 0; i < coordinates.size(); i++) {
            int row = coordinates.get(i).get(0);
            int col = coordinates.get(i).get(1);

            board[row][col] = '+';

        }


        for (int col = 0; col < board_size; col++) {

            List<Character> rowArray = new ArrayList<>();

            for (int row = 0; row < board_size; row++) {

                if (board[row][col] != '*' && board[row][col] != '+') {
                    rowArray.add(board[row][col]);
                }
            }

            int i = 0;
            for (int row = board_size-1; row > -1; row--) {

                if (i < rowArray.size()) {
                    board[row][col] = rowArray.get(rowArray.size() - i - 1);
                    i++;
                } else {
                    board[row][col] = '*';
                }

            }
        }

    }

    public static void gravity(char[][] board, int board_size, List<List<Integer>> coordinates) {

        for (int i = 0; i < coordinates.size(); i++) {
            int row = coordinates.get(i).get(0);
            int col = coordinates.get(i).get(1);

            board[row][col] = '*';

        }

        for(int col=0;col<board_size;col++){
            int star = board_size - 1;
            for(int row=board_size-1; row > -1;row--){
                if (board[row][col] != '*'){
                    char temp = board[row][col];
                    board[row][col] = board[star][col];
                    board[star][col] = temp;
                    star--;
                }
            }
        }

    }

    public static char[][] deepCopy(char[][] matrix) {

        char[][] new_mat = new char[matrix.length][];
        for(int i=0;i<matrix.length;i++){
            new_mat[i] = matrix[i].clone();
        }
        return new_mat;

        //return java.util.Arrays.stream(matrix).map(el -> el.clone()).toArray($ -> matrix.clone());
    }

    public static List<List<Integer>> deepCopyFinalMove(List<List<Integer>> final_move){

        List<List<Integer>> temp = new ArrayList<>();
        for(int i=0; i<final_move.size();i++){
            List<Integer> pair = new ArrayList<>();
            pair.add(final_move.get(i).get(0));
            pair.add(final_move.get(i).get(1));

            temp.add(pair);
        }
        return temp;
    }

    public static String printPosition(List<List<Integer>> final_moves){
        char col = (char) ('A'+final_moves.get(0).get(1));
        return String.valueOf(col) + String.valueOf(final_moves.get(0).get(0)+1);
    }

    public static int alphaBeta(char[][] board, int board_size, TreeMap<Integer, List<List<List<Integer>>>> possible_moves, int my_score, int opp_score, int depth, int alpha, int beta, boolean maximizingPlayer, boolean isFirstMove, List<List<Integer>> final_move) {

        number_of_nodes_expanded += 1;
        if (depth == 0 || possible_moves.isEmpty()) {
            return my_score-opp_score;

        } else {

            if (maximizingPlayer) {

                Iterator entries = possible_moves.entrySet().iterator();

                while (entries.hasNext()) {

                    Map.Entry<Integer, List<List<List<Integer>>>> entry = (Map.Entry<Integer, List<List<List<Integer>>>>) entries.next();

                    for (List<List<Integer>> inner_entry: entry.getValue()){

                        char[][] board_copy = deepCopy(board);
                        gravity(board_copy, board_size, inner_entry);

                        int score = alphaBeta(board_copy, board_size, possibleMoves(board_copy, board_size), (int) (Math.pow(entry.getKey(),2)+my_score), opp_score, depth-1, alpha, beta, false, false, final_move);
                        if (score > alpha){
                            alpha = score;
                            if(isFirstMove){
                                final_move.clear();
                                final_move.addAll(inner_entry);
                            }

                        }

                        if (beta <= alpha){

                            return alpha;
                        }
                    }
                }

                return alpha;
            }

            else{

                Iterator entries = possible_moves.entrySet().iterator();
                while (entries.hasNext()) {

                    Map.Entry<Integer, List<List<List<Integer>>>> entry = (Map.Entry<Integer, List<List<List<Integer>>>>) entries.next();

                    for (List<List<Integer>> inner_entry: entry.getValue()){
                        char[][] board_copy = deepCopy(board);
                        gravity(board_copy, board_size, inner_entry);

                        int score = alphaBeta(board_copy, board_size, possibleMoves(board_copy, board_size), my_score, (int) (Math.pow(entry.getKey(),2)+opp_score), depth-1, alpha, beta, true, false, final_move);
                        if (score<beta){
                            beta = score;
                        }

                        if (beta <= alpha){
                            return beta;
                        }

                    }
                }
                return beta;
            }

        }
    }

    public static String[] ReadFileToStringArray(String ReadThisFile) throws FileNotFoundException{
        return (new Scanner( new File(ReadThisFile) ).useDelimiter("\\A").next()).split("[\\r\\n]+");
    }

    public static int calculateDepth(int branching_factor, float time_remaining) throws FileNotFoundException {

        int depth;
        String[] calibrate_data = ReadFileToStringArray("calibrate.txt");

        int nodes_expanded_per_second = Integer.parseInt(calibrate_data[0]);
        int time_for_this_move =0;
        if (branching_factor == 1){
            return 1;
        }
        else{
            time_for_this_move = (int) (time_remaining/(branching_factor/2));
        }

        System.out.println("bf"+branching_factor);
        System.out.println(time_for_this_move);
        depth = 1;
        while(true){

            if (time_for_this_move*nodes_expanded_per_second < Math.pow(branching_factor,depth))
                break;

            depth++;
        }

        return depth;
    }

    public static int used_for_calibrate(char[][] board, int board_size, int depth){

        List<List<Integer>> final_move = new ArrayList<>();
        TreeMap<Integer, List<List<List<Integer>>>> possible_moves = possibleMoves(board, board_size);
        System.out.println(possible_moves.get(1).size());
        int final_ans = alphaBeta(board,board_size, possible_moves,0,0, depth, Integer.MIN_VALUE, Integer.MAX_VALUE, true, true, final_move);

        return number_of_nodes_expanded;
    }

    public static void main(String args[]) throws IOException {

        String[] file_input = ReadFileToStringArray("input.txt");
        int board_size = Integer.parseInt(file_input[0]);
        int no_of_fruit = Integer.parseInt(file_input[1]);
        float time_remaining = Float.parseFloat(file_input[2]);

        char[][] board = new char[board_size][board_size];
        for(int i=3; i<board_size+3;i++){
            for(int j=0;j<board_size;j++) {
                board[i - 3][j] = file_input[i].charAt(j);
            }
        }

        List<List<Integer>> final_move = new ArrayList<>();
        long start_time = System.currentTimeMillis();


        TreeMap<Integer, List<List<List<Integer>>>> possible_moves = possibleMoves(board, board_size);
        int branching_factor = 0;
        Iterator entries = possible_moves.entrySet().iterator();

        while (entries.hasNext()){
            Map.Entry<Integer, List<List<List<Integer>>>> entry = (Map.Entry<Integer, List<List<List<Integer>>>>) entries.next();
            branching_factor += entry.getValue().size();

        }

        int depth = calculateDepth(branching_factor, time_remaining);

        System.out.println("depth:"+depth);
        int final_ans = alphaBeta(board,board_size, possible_moves,0,0, 3, Integer.MIN_VALUE, Integer.MAX_VALUE, true, true, final_move);
        long end_time = System.currentTimeMillis();

        gravity(board,board_size,final_move);
        FileWriter fw = new FileWriter("output.txt");
        BufferedWriter bw = new BufferedWriter(fw);
        bw.write((printPosition(final_move)+"\n"+printBoard(board,board_size)));
        bw.close();
        fw.close();
        System.out.println((end_time-start_time)+"");
        //System.out.println(final_move);
        //System.out.println(final_ans);

        //printBoard(board,board_size);*/

    }

    public static void gravity2(char[][] board, int board_size, List<List<Integer>> coordinates) {


        for (int i = 0; i < coordinates.size(); i++) {
            int row = coordinates.get(i).get(0);
            int col = coordinates.get(i).get(1);

            board[row][col] = '+';

        }


        for (int col = 0; col < board_size; col++) {

            List<Character> rowArray = new ArrayList<>();

            for (int row = 0; row < board_size; row++) {

                if (board[row][col] != '*' && board[row][col] != '+') {
                    rowArray.add(board[row][col]);
                }
            }

            int i = 0;
            for (int row = board_size-1; row > -1; row--) {

                if (i < rowArray.size()) {
                    board[row][col] = rowArray.get(rowArray.size() - i - 1);
                    i++;
                } else {
                    board[row][col] = '*';
                }

            }
        }

    }
}
