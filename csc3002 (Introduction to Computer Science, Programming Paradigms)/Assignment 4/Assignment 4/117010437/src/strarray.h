#ifndef INTARRAY_H
#define INTARRAY_H
#include <string>
#include <new>
#include <error.h>
#include "testing/SimpleTest.h"
#define DEFAULT_CAPACITY 8

class StrArray
{
    /*
     * We use three-pointer method to represent the array
     *
     * The used elements are in [start, usage);
     * The available memory are in [start, end);
     * -----------------------------------------------------------------
     * - start: pointer to the start position of the memory area
     * - usage: pointer to the position passed last used area
     * - end: pointer to the end position of the memory area
     */
    std::string * start;
    std::string * usage;
    std::string * end;

    /*
     * void grow()
     * -----------------------------------------------------------------
     * Implement a grow function, which increase the array capacity to
     * 2 * capacity();
     * Basically, it reallocates a new memory area of twice of
     * the original size.
     * Then it calls `std::uninitialized_move` to move all the elements to
     * the new place.
     * After that, it iterates through the old memory area, by calling
     * `std::destroy` to clean up the old area.
     * After that, it deallocate the original memory space with `::operator delete`
     *  and update the start, end and usage pointer correclty.
     *
     * References
     * -----------------------------------------------------------------
     * - https://en.cppreference.com/w/cpp/memory/destroy
     * - https://en.cppreference.com/w/cpp/memory/uninitialized_move
     */
public:
    using size_type = size_t;
    /*
     * StrArray Constructor
     * ----------------------------------------------------------
     * Initialize the memory area with DEFAULT_CAPACITY;
     * This part is already given as a reference, please
     * have a serious look of the implementation.
     */
    StrArray();

    /*
     * StrArray Destructor
     * ----------------------------------------------------------
     * First call `std::destroy` to destruct all elements in the memory area [start, usage).
     * Then, deallocate the memory area with `::operator delete`
     */
    ~StrArray();

    /*
     * size_type size() const noexcept
     * ----------------------------------------------------------
     * Return the used size of the array.
     * This is already given.
     */
    size_type size() const noexcept;

    /*
     * size_type capacity() const noexcept
     * ----------------------------------------------------------
     * Return the used size of the array.
     * This is already given.
     */
    size_type capacity() const noexcept;

    /*
     * void push_back(const std::string& str)
     * ----------------------------------------------------------
     * add a new element to the end of the array;
     * If the `end == usage`, the capacity the full,
     * just call a `grow()` first.
     */
    void push_back(const std::string& str);

    /*
     * std::string& get(size_type index)
     * ----------------------------------------------------------
     * get the string at the given position.
     * if index >= size(), call error(msg) to throw an error
     */
    std::string& get(size_type index);

    /*
     * void set(size_type index, const std::string& str)
     * ----------------------------------------------------------
     * set the string at the given position.
     * if `index >= size()`, call error(msg) to throw an error
     */
    void set(size_type index);

    /*
     * std::string& operator[](size_type index)
     * ----------------------------------------------------------
     * get the string at the given position.
     * This function enables us to access the element with array[index]
     * syntax;
     */
    std::string& operator[](size_type index);
};



#endif // INTARRAY_H
