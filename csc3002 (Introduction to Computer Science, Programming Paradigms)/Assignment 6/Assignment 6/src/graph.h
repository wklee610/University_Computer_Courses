#ifndef GRAPH_H
#define GRAPH_H

#include <memory>
#include <tuple>
#include <unordered_map>
#include <string>
#include <vector>


using NodePtr = struct Node *;

struct Node {
    std::string name;
    std::vector < NodePtr > edges;

    explicit Node ( std::string name );
};

/*
 * Graph
 * --------------------------------------------------------------
 * - Directed Graph
 * - The graph can have cycle; Please see each question for
 *   specifications
 */
class Graph
{
    std::unordered_map < std::string, Node > inner;
    // create a node if it does not exist
    void add_node ( const std::string & name );
    // link two nodes
    void link ( const std::string & from, const std::string & to );
public:
    // constructors
    Graph() = default;

    Graph ( const std::vector < std::pair < std::string, std::string > > & );

    // the following are on yourself.

    /*
     * std::vector< std::string > dfs_order ( const std::string & root ) const
     * --------------------------------------------------------------------
     * Using `std::stack` to run DFS.
     * Return the DFS order starting from the root.
     *
     * - The order is recorded when a node is pushed to stack
     * - For edges, please visit them in the order as they are in the vector.
     * - Already visited nodes will not be pushed to stack again.
     * - For details, see examples.
     */
    std::vector< std::string > dfs_order ( const std::string & root ) const;

    /*
     * std::vector< std::string > bfs_order ( const std::string & root ) const
     * --------------------------------------------------------------------
     * Using `std::queue` to run BFS.
     * Return the BFS order starting from the root.
     *
     * - The order is recorded when a node is pushed to queue.
     * - For edges, please visit them in the order as they are in the vector.
     * - Already visited nodes will not be pushed to queue again.
     * - For details, see examples.
     */
    std::vector< std::string > bfs_order ( const std::string & root ) const;

};

#endif // GRAPH_H
