/*
 * File: stringmap.h
 * -----------------
 * This interface exports a simplified version of the Map class in which
 * the keys and values are always strings.
 */

#ifndef _stringmap_h
#define _stringmap_h
#define DEFAULT_MAP_CAP 13
#define MAX_LOAD_FACTOR  0.75
#include <string>
#include <optional>


/*
 * class StrMap
 * ------------------------------------------------
 * A string to string hashmap.
 *
 * - Addressing strategy: Open Addressing.
 * - Probing strategy: Linear Probing.
 * - Remove stragegy: Dummy Entry
 * - DEFAULT_MAP_CAP is given
 */
class StrMap {
public:

    using return_type = std::optional<std::reference_wrapper<std::string>>;

    // default constructor
    StrMap ( );

    // destructor
    ~StrMap ( );

    /*
     * return_type operator[] ( const std::string & key ) const
     * ---------------------------------------------------------
     * Get a reference to the value associated with the key if it exists in the hashmap.
     *
     * - Return `std::nullopt` if the key does not exist
     * - You can use `std::ref ( value )` to create a `std::reference_wrapper`
     *   to value
     * - See https://en.cppreference.com/w/cpp/utility/optional for documents of `std::optional`
     * - See https://en.cppreference.com/w/cpp/utility/functional/reference_wrapper for documents
     *   of `std::reference_wrapper`
     * - See https://en.cppreference.com/w/cpp/utility/functional/ref for documents of `std::ref`
     */
    return_type operator[] ( const std::string & key ) const;

    /*
     * void insert ( const std::string & key, const std::string& value )
     * ------------------------------------------------------------------
     * Insert a new item to the hashmap.
     *
     * - If key exists, simply replace the value.
     * - Otherwise, if `load_factor ( ) >= MAX_LOAD_FACTOR`, do `rehash ( )` first
     * - Then use linear probing and open addressing to locate a new bucket for the key-value pair
     */
    void insert ( const std::string & key, const std::string& value );

    /*
     * void erase ( const std::string & key )
     * ------------------------------------------------------------------
     * Erase an existing key-value pair
     *
     * - If the key exists, remove the key.
     * - If the key does not exists, do nothing.
     * - If this operation results in an empty slot in the middle, the
     *   handling strategy is to mark the slot as dummy to make sure that
     *   later probing can be done successfully.
     */
    void erase ( const std::string & key );

    /*
     * bool contains ( const std::string & key ) const
     * -------------------------------------------------------------------
     * Check whether the hashmap contains the given key.
     */
    bool contains ( const std::string & key ) const;

    /*
     * bool empty ( ) const
     * -------------------------------------------------------------------
     * Check whether the hashmap is empty or not.
     */
    bool empty ( ) const;


    /*
     * size_t size ( ) const
     * -------------------------------------------------------------------
     * Return the size of the hashmap (number of used buckets)
     */
    size_t size ( ) const;

    /*
     * size_t capacity ( ) const
     * -------------------------------------------------------------------
     * Return the capacity of the hashmap (number of all buckets)
     */
    size_t capacity ( ) const;

    /*
     * void clear ( )
     * -------------------------------------------------------------------
     * Clear all hashmap entries and reset capacity to default.
     */
    void clear ( );

    /*
     * void rehash ( )
     * -------------------------------------------------------------------
     * Grow the hashmap capacity to 3 times (we should have `3 * original`
     * capacity after this operation) and rehash all existing entries.
     */
    void rehash ( );


    /*
     * float load_factor () const
     * -------------------------------------------------------------------
     * Get the load factor of the current hashmap.
     */
    float load_factor () const;

    /*
     * We do not want copy of the structure, therefore
     * we mark it as delete here;
     */
    StrMap ( const StrMap & that ) = delete;
    StrMap & operator==( const StrMap & that ) = delete;

private:

    struct Bucket {
        bool used;
        bool dummy;
        std::string key;
        std::string value;
    };

    Bucket * _bucket;
    size_t _size;
    size_t _capacity;

    // this is used to get the hash value of a string
    static inline uint64_t hash_value ( const std::string & key ) {
        return std::hash<std::string> {} ( key );
    }
};



#endif
