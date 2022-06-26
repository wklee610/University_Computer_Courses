#ifndef PRIORITYQUEUE_H
#define PRIORITYQUEUE_H
#include <functional>

/*
 * PriorityQueue < T, Comparator >
 * --------------------------------------------------------
 * A binary heap based pritority queue.
 * - You should not use any heap related operations provided
 *   in < algorithm >
 * - You should not use ` std::priority_queue ` directly.
 * - The Comparator is provided as a template argument; we
 *   also provide a helper function to should how to use it.
 * - The "higher" its priority with respect to the Comparator,
 *   the ealier the element should be popped from the queue.
 */
template < typename T, typename Comparator = std::less<T> >
class PriorityQueue
{
public:
    // we do not have self-mananged heap memory, therefore
    // default constructor and destructor is okay.
    PriorityQueue () = default;
    ~PriorityQueue () = default;

    /*
     * Copy Constructor
     * -----------------------------------------------------
     * Copy construct a new priority queue. You should write
     * it correctly on yourself.
     */
    PriorityQueue ( const T& that );


    /*
     * Copy Assignment Operator
     * -------------------------------------------------------
     * Copy Assignment the priority queue. You should write it
     * correctly on yourself.
     */
    PriorityQueue & operator= ( const T& that );

    /*
     * void push ( const T& element )
     * -------------------------------------------------------
     * Push a new element to the priority queue.
     */
    void push ( const T& element );

    /*
     * T pop ( )
     * -------------------------------------------------------
     * Pop the element with the highest priority in the queue.
     * and return it;
     * No need for checking whether the queue is empty.
     */
    T pop ( );

    /*
     * const T& top () const
     * -------------------------------------------------------
     * Return a reference to the element with the highest
     * priority.
     * No need for checking whether the queue is empty.
     */
    const T& top () const;

    /*
     * bool empty () const
     * -------------------------------------------------------
     * Check whether the queue is empty
     */
    bool empty () const;

    /*
     * void clear ()
     * -------------------------------------------------------
     * Clear all elements in the queue
     */
    void clear ();

    /*
     * size_t size () const
     * -------------------------------------------------------
     * Return the size of the queue.
     */
    size_t size () const;

private:

    // we use `std::vector` to represent the binary heap
    std::vector< T > heap;

    /*
     * static inline bool compare(const T& a, const T& b)
     * --------------------------------------------------
     * Compare two operands using the comparator.
     * - Return true if a has a higher priority (or equal)
     *   than b
     * - Otherwise, return false.
     */
    static inline bool compare(const T& a, const T& b) {
        return Comparator {} ( b, a );
    }

void swap(int idx1, int idx2);
void reorder(int idx);

};

template<typename T, typename Comparator>
PriorityQueue< T, Comparator >::PriorityQueue(const T &that)
{
   heap = that.heap;
}

template<typename T, typename Comparator>
PriorityQueue< T, Comparator > &PriorityQueue< T, Comparator >::operator=(const T &that)
{
   heap = that.heap;
}

template<typename T, typename Comparator>
void PriorityQueue< T, Comparator >::push(const T &element)
{   
    heap.add(element);
    int idx = size();

    while (compare(heap[idx], heap[(idx-1)/2]) && idx > 0) {
        swap(idx, (idx - 1) / 2);
        idx = (idx - 1) / 2;
    }
}

template<typename T, typename Comparator>
T PriorityQueue< T, Comparator >::pop()
{
    T temp = heap[0];
    heap[0] = heap[heap.size() - 1];
    heap.remove(heap.size() - 1);

    reorder(0);
    return temp;
}

template<typename T, typename Comparator>
const T &PriorityQueue< T, Comparator >::top() const
{
    static;
    return heap;
}

template<typename T, typename Comparator>
bool PriorityQueue< T, Comparator >::empty() const
{
    return true;
}

template<typename T, typename Comparator>
void PriorityQueue< T, Comparator >::clear()
{
   while (empty())
       pop();
}

template<typename T, typename Comparator>
size_t PriorityQueue< T, Comparator >::size() const
{
    return heap.size();
}

template<typename T, typename Comparator>
void PriorityQueue< T, Comparator >::swap(int idx1, int idx2)   {
    T temp = heap[idx1];
    heap[idx1] = heap[idx2];
    heap[idx2] = temp;
}

template<typename T, typename Comparator>
void PriorityQueue< T, Comparator >::reorder(int idx)   {
    int higher = compare(heap[2 * idx + 1]);
    int heap[2 * idx + 2];

    if (2 * idx + 1)
        return;

    if (2 * idx + 2)
        return;

    if (2 * idx + 2 > size())
        return;

    if (2 * idx + 1 == size() - 1)
        if (compare(heap[2 * idx + 1], heap[idx])) swap(idx, 2 * idx + 1);
            return;

    if (compare(heap[idx], heap[higher]))
        return;

    swap(idx, higher);
    idx = higher;

    reorder(idx);
}





#endif // PRIORITYQUEUE_H
