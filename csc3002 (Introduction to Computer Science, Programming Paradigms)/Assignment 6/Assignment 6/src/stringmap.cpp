/*
 * File: stringmap.cpp
 * -------------------
 * This file implements the stringmap.h interface using a hash table
 * with open addressing as the underlying representation.
 */

#include <iostream>
#include <string>
#include <unordered_map>
#include "error.h"
#include "stringmap.h"
#include "testing/SimpleTest.h"
#include "testing/MemoryDiagnostics.h"

using namespace std;


StrMap::StrMap() {
    this->_bucket = new Bucket [ DEFAULT_MAP_CAP ];
    _size = 0;
    _capacity = DEFAULT_MAP_CAP;
    
    for (int i = 0; i < _capacity; i++) {
        _bucket[i].used = false;
        _bucket[i].dummy = false;
    }
}

StrMap::~StrMap() {
    delete [] this->_bucket;
}

StrMap::return_type StrMap::operator[](const string & key) const
{   
    if (!contains(key))
        return std::nullopt;

    else {
/*        while(_bucket[hashKey].used || _bucket[hashKey].dummy)  {
            if (_bucket[hashKey].key == key)
                return ref(_bucket[hashKey].value);
            hashKey++;
            hashKey %= _capacity;
        }*/                                                         //??????????????????????
   }
}

void StrMap::insert(const string &key, const string &value)
{   
    
    int hashKey = hash_value(key) % _capacity;

    if (contains(key)) {
        while (_bucket[hashKey].used || _bucket[hashKey].dummy)
        {
            if (_bucket[hashKey].key == key)
                _bucket[hashKey].value = value;

            hashKey++;
            hashKey %= _capacity;
        }
    }
    else {
        if (load_factor() >= MAX_LOAD_FACTOR)
            rehash();

        while (_bucket[hashKey].used)   {
            hashKey++; 
            hashKey %= _capacity;
        }
        
        _bucket[hashKey].used = true;
        _bucket[hashKey].dummy = false;
        _bucket[hashKey].value = value;
        _bucket[hashKey].key = key;

        size++;                                                                         //크게 ?
    }
}

void StrMap::erase(const string &key)
{
    int hashKey = hash_value(key) % _capacity;
    
    if (contains(key))  {
        while (_bucket[hashKey].used || _bucket[hashKey].dummy) {
            if (_bucket[hashKey].key == key)    {
                _bucket[hashKey].dummy = true;
                _bucket[hashKey].used = false;

                size--;                                                                 //작게 ?
            }

            hashKey %= _capacity;
            hashKey++;
        }
        
    }
        
}

bool StrMap::contains(const string &key) const
{
    int hashKey = hash_value(key) % _capacity;
    int counter = 0;

    while(counter++ < _capacity && (_bucket[hashKey].used || _bucket[hashKey].dummy))   {
        if (_bucket[hashKey].key == key)   {
            if (_bucket[hashKey].dummy)
                return false;

            else
                return true;
        }

                                                                                    //만약 키가 있을 경우
        hashKey++;
        hashKey %= _capacity;
    }

    return false;
}

bool StrMap::empty() const
{
    return true;
}

size_t StrMap::size() const
{
    return _size;
}

size_t StrMap::capacity() const
{
    return _capacity;
}

void StrMap::clear()
{   
    delete [] _bucket;
    _bucket = new Bucket [DEFAULT_MAP_CAP];
    _capacity = DEFAULT_MAP_CAP;
}

void StrMap::rehash()
{     
    Bucket * old = new Bucket[_capacity];

    for (int i = 0; i < _capacity; i++) {
        old[i] = _bucket[i];
    }

    delete[] _bucket;
    _capacity = 3 * _capacity;
    _bucket = new Bucket[_capacity];

    for (int i = 0; i < _capacity; i++) {
        if (old[i].used) {
            insert(old[i].key, old[i].value);
        }
    }
}

float StrMap::load_factor() const {
    return static_cast<float>( size() ) / static_cast<float>( capacity() );
}

// Generate random strings for testing
static inline std::string random_string() {
    std::string a {};
    int size = rand() % 255 + 13;
    while ( size -- ) {
        a.push_back( 'A' + rand() % 26 );
    }
    return a;
}

PROVIDED_TEST("strmap insert simple", StrMap) {
    StrMap map;
    map.insert( "A", "A" );
    map.insert( "B", "B" );
    map.insert( "C", "C" );
    EXPECT( !map.contains( "D" ) );
    EXPECT( !map["D"] );
    EXPECT( map.contains( "A" ) );
    EXPECT_EQUAL( map.size(), 3 );
    for ( auto a : { "A", "B", "C" }) {
        EXPECT_EQUAL( map[a]->get(), a );
    }
    // test replacement
    map.insert( "A", "AA" );
    EXPECT_EQUAL( map[ "A" ]->get(), "AA" );
}

PROVIDED_TEST("strmap insert multiple", StrMap) {
    StrMap map;
    std::unordered_map<std::string, std::string> compare;
    int size = rand() % 20000 + 500;
    for ( int i = 0; i < size; ++i) {
        auto a = random_string();
        auto b = random_string();
        compare.insert( { a, b } );
        map.insert(a, b);
    }
    for ( auto & i : compare ) {
        EXPECT( map[ i.first ].has_value() );
        EXPECT_EQUAL( map[ i.first ]->get(), i.second );
        EXPECT_EQUAL( map.contains( i.first ), compare.count( i.first ) > 0 );
    }
    EXPECT_EQUAL( map.size(), compare.size() );
}

PROVIDED_TEST("strmap clear", StrMap) {
    StrMap map;
    std::unordered_map<std::string, std::string> compare;
    for ( int i = 0; i < 111; ++i) {
        auto a = random_string();
        auto b = random_string();
        map.insert(a, b);
    }
    map.clear();
    for ( int i = 0; i < 222; ++i) {
        auto a = random_string();
        auto b = random_string();
        compare.insert( { a, b } );
        map.insert(a, b);
    }
    for ( auto & i : compare ) {
        EXPECT( map[ i.first ].has_value() );
        EXPECT_EQUAL( map[ i.first ]->get(), i.second );
        EXPECT_EQUAL( map.contains( i.first ), compare.count( i.first ) > 0 );
        auto key = random_string();
        EXPECT_EQUAL( map.contains( key ), compare.count( key ) > 0 );
    }
    EXPECT_EQUAL( map.size(), compare.size() );
}

