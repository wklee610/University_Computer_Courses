#include "strarray.h"


StrArray::StrArray()
{
    void * uninitialized_memory =
            ::operator new(sizeof(std::string) * DEFAULT_CAPACITY);
    usage = start = reinterpret_cast<std::string *>(uninitialized_memory);
    end = usage + DEFAULT_CAPACITY;
}

StrArray::~StrArray()
{
    // add your implementation
}

StrArray::size_type StrArray::size() const noexcept
{
    return usage - start;
}

StrArray::size_type StrArray::capacity() const noexcept
{
    return end - start;
}

void StrArray::push_back(const std::string &str)
{
    // add your implementation
}

std::string &StrArray::get(StrArray::size_type index)
{
    // add your implementation
    static std::string remove_this {"remove this"};
    return remove_this;
}

void StrArray::set(StrArray::size_type index)
{
    // add your implementation
}

std::string &StrArray::operator[](StrArray::size_type index)
{
    // add your implementation
    static std::string remove_this {"remove this"};
    return remove_this;
}

PROVIDED_TEST("push_back no grow", STRARRAY) {
    std::vector<std::string> compare;
    StrArray arr;
    for (int i = 0; i < 8; ++i) {
        compare.push_back(std::string {char(48 + i)});
        arr.push_back(std::string {char(48 + i)});
    }
    for (int i = 0; i < 8; ++i) {
        EXPECT_EQUAL(arr.get(i), compare.at(i));
    }
}

PROVIDED_TEST("push_back grow", STRARRAY) {
    std::vector<std::string> compare;
    StrArray arr;
    for (int i = 0; i < 26; ++i) {
        compare.push_back(std::string {char('a' + i)});
        arr.push_back(std::string {char('a' + i)});
    }
    for (int i = 0; i < 26; ++i) {
        EXPECT_EQUAL(arr[i], compare[i]);
    }
}
