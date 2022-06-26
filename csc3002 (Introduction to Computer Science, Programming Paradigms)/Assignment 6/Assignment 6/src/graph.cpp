#include "graph.h"
#include <stack>
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include "testing/SimpleTest.h"




Node::Node(std::string name) : name( std::move(name) ), edges() {}


Graph::Graph( const std::vector < std::pair < std::string, std::string > > & edges )
{
    for ( auto & i : edges ) {
        add_node( std::get< 0 > ( i ) );
        add_node( std::get< 1 > ( i ) );
        link( std::get< 0 > ( i ), std::get< 1 > ( i ) );
    }
}

void Graph::add_node(const std::string &name) {
    if ( inner.count( name ) == 0 ) {
        inner.insert( { name, Node { name } } );
    }
}

void Graph::link(const std::string &from, const std::string &to ) {
    auto a = inner.find( from );
    auto b = inner.find( to );
    if ( a != inner.end() && b != inner.end() ) {
        a->second.edges.push_back( &b->second );
    }
}

std::vector<std::string> Graph::dfs_order( const std::string & root ) const
{
    std::vector< std::string > result;
    std::cout << root << std::endl;     //std 굳이 써야하나?

    result.push_back(root);

    std::vector<NodePtr>rPtr = inner.find(root)->second.edges;

    for(NodePtr i : rPtr) {
        std::vector<std::string> subresult = dfs_order(i->name);

        for(std::string j: subresult)   {
            result.push_back(j);
        }

    }
    return result;
}

std::vector<std::string> Graph::bfs_order( const std::string & root ) const
{
    std::vector< std::string > result;
    result.push_back(root);
    Node rnode = inner.find(root)->second;
    std::vector<NodePtr> ptrs = rnode.edges;

    while(ptrs.size() != 0)    {
        std::vector<NodePtr> trans;

        for(NodePtr i : ptrs)  {
            result.push_back(i->name);

            std::vector<NodePtr> iPtr = i->edges;

            for(NodePtr j : iPtr)   {
                trans.push_back(j);
            }

        }

    }
    return result;
}


/*
 * TREE (ACYCLIC)
 * ------------------------
 *                 A
 *                / \
 *               B   C
 *              /     \
 *             D       E
 *                      \
 *                       F
 * DFS ORDER: A B D C E F
 * BFS ORDER: A B C D E F
 *
 */
static Graph TREE = Graph ( {
  { "A", "B" },
  { "A", "C" },
  { "B", "D" },
  { "C", "E" },
  { "E", "F" }
});

/*
 * RANDOM (CYCLIC)
 * ------------------------
 *
 *
 *   --> B --> C --> F
 *  /   /      ^
 * A <--       |
 *  \          |
 *   --> D --> E --> G
 *
 *
 * DFS ORDER: A B C F D E G
 * BFS ORDER: A B D C E F G
 *
 */
static Graph RANDOM = Graph ( {
    {"A", "B"},
    {"A", "D"},
    {"B", "A"},
    {"B", "C"},
    {"C", "F"},
    {"D", "E"},
    {"E", "C"},
    {"E", "G"}
});




PROVIDED_TEST("graph dfs", Graph) {
    EXPECT( TREE.dfs_order( "A" ) ==
                  (std::vector<std::string> { "A", "B", "D", "C", "E", "F"}) );

    EXPECT( RANDOM.dfs_order( "A" ) ==
                  (std::vector<std::string> { "A", "B", "C", "F", "D", "E", "G"}) );
}

PROVIDED_TEST("graph bfs", Graph) {
    EXPECT( TREE.bfs_order( "A" ) ==
                  (std::vector<std::string> { "A", "B", "C", "D", "E", "F"}) );

    EXPECT( RANDOM.bfs_order( "A" ) ==
                  (std::vector<std::string> { "A", "B", "D", "C", "E", "F", "G"}) );
}




