/**
 * File: TestDriver.h
 *
 * @author Keith Schwarz
 * @version 2020/3/22
 *    Keith final revision from end of quarter 19-2
 * @version 20200/4/8
 *    Minor tweaks by Julie & Nick for quarter 19-3
 */
#pragma once

// be careful about what is #include here, this is dumping into all student sources right now
#include <cmath>  // fabs
#include <cfloat>
#include <functional>
#include <sstream>
#include <iomanip>
#include <string>
#include "timer.h"
#include "TextUtils.h"

/* Type representing a key in the top-level testing map. We use the file basename
 * as the top-level grouping.
 */
using TestKey = std::string;

/* Type representing a test case, including name, owner (student or provided),
 * line number, and the callback function to execute.
 */
struct TestCase {
    std::string testname;
    int line;
    std::string filename;
    std::string owner;
    std::function<void()> callback;
};



/* Exception type signifying that a test case failed. */
class TestFailedException: public std::logic_error {
public:
    TestFailedException(const std::string &message);
};

/* Object whose sole purpose is to put a test case into a group of tests. */
class TestCaseAdder {
public:
    TestCaseAdder(const TestKey& key, int lineNumber, const std::string& name, const std::string &owner, std::function<void()>);
};

/**** Defines the macro that adds a new test case. ****/

/* First, undefine STUDENT_TEST, since we defined it above as a way of "prototyping" it. */
#undef STUDENT_TEST
#undef PROVIDED_TEST

/* We need several levels of indirection here because of how the preprocessor works.
 * This first layer expands out to the skeleton of what we want.
 */
#define STUDENT_TEST(name) DO_ADD_TEST(_testCase, _adder, name, __LINE__, "STUDENT_TEST")
#define PROVIDED_TEST(name, ID) DO_ADD_TEST(_testCase##ID, _adder##ID, name, __LINE__, "PROVIDED_TEST")
#define AUTOGRADER_TEST(name) DO_ADD_TEST(_testCase, _adder, name, __LINE__, "AUTOGRADER_TEST")
#define MANUAL_TEST(name) DO_ADD_TEST(_testCase, _adder, name, __LINE__, "MANUAL_TEST")

/* This level of indirection exists so that line will be expanded to __LINE__ and
 * from there to the true line number. We still can't token-paste it here, since
 * the even further level of indirection.
 */
#define DO_ADD_TEST(fn, adder, name, line, owner)\
    static void JOIN(fn, line)();\
    static TestCaseAdder JOIN(adder, line)(__FILE__, line, name, owner, JOIN(fn, line));\
    static void JOIN(fn, line)()

#define JOIN(X, Y) X##Y

/***** Macros used to implement testing primitives. *****/
void doFail(const std::string& message, std::size_t line = 0);
void addDetail(const std::string& message);

#undef EXPECT
#define EXPECT(condition) doExpect(condition, "EXPECT failed: " #condition " is not true.", __LINE__)
void doExpect(bool condition, const std::string& expression, std::size_t line);

#undef EXPECT_ERROR
#define EXPECT_ERROR(condition) do {\
    std::stringstream _out; \
    try {\
        (void)(condition); \
        _out << "Line " << __LINE__ << " EXPECT_ERROR failed: " #condition " did not call error()."; \
        doFail(_out.str()); \
    } catch (const ErrorException& e) { \
        _out << "Line " << __LINE__ << " EXPECT_ERROR ok: error raised " \
             << "\"" << e.getMessage() << "\""; \
        addDetail(_out.str()); \
    }\
} while(0)

#undef EXPECT_NO_ERROR
#define EXPECT_NO_ERROR(condition) do {\
    std::stringstream _out; \
    try {\
        (void)(condition); \
        _out << "Line " << __LINE__ << " EXPECT_NO_ERROR successful: " #condition " did not call error()."; \
        addDetail(_out.str()); \
    } catch (const ErrorException& e) { \
        _out << "Line " << __LINE__ << " EXPECT_NO_ERROR failed: error was raised " \
             << "\"" << e.getMessage() << "\""; \
        doFail(_out.str()); \
    }\
} while(0)

/* * * * Pretty-Printers for EXPECT_EQUAL * * * */
inline std::string debugFriendlyString(char c) {
    return quotedVersionOf(c);
}

/* Print strings in quotes. */
inline std::string debugFriendlyString(const std::string& s) {
    return quotedVersionOf(s);
}
inline std::string debugFriendlyString(const char* s) {
    return debugFriendlyString(std::string(s));
}
template <size_t N> std::string debugFriendlyString(char (&s)[N]) {
    return debugFriendlyString((const char *)s);
}

/* Print float/double with maximum precision. */
inline std::string debugFriendlyString(float value) {
    std::ostringstream result;
    result << std::setprecision(FLT_DIG+1) << value << "f";
    return result.str();
}

inline std::string debugFriendlyString(double value) {
    std::ostringstream result;
    result << std::setprecision(DBL_DIG+1) << value << "d";
    return result.str();
}

/* Print bools as strings. */
inline std::string debugFriendlyString(bool value) {
    return value? "true" : "false";
}

/* Print nullptr as such. */
inline std::string debugFriendlyString(std::nullptr_t) {
    return "nullptr";
}

template <typename T>
inline std::string debugFriendlyString(T* ptr) {
    /* Print null pointers as such. */
    if (ptr == nullptr) return "nullptr";

    std::ostringstream converter;
    converter << "Memory address " << std::hex << (void *)ptr;
    return converter.str();
}

/* Print everything else using stream insertion. */
template <typename T> std::string debugFriendlyString(const T& value) {
    std::ostringstream result;
    result << value;
    return result.str();
}

/* * * * Equality comparisons * * * */

/* Equality comparisons are fuzzy for real numbers. */
inline bool _areEqual(double lhs, double rhs) {
    double tolerance = std::max(std::abs(lhs), std::abs(rhs))*DBL_EPSILON;
    return std::abs(lhs - rhs) <= tolerance;
}

template <typename T1, typename T2> bool _areEqual(const T1& lhs, const T2& rhs) {
    return lhs == rhs;
}

inline std::string abbreviate(const std::string& s, size_t maxLen = 300) {
    return s.length() < maxLen ? s : s.substr(0, maxLen) + " ...";
}

#undef EXPECT_EQUAL
#define EXPECT_EQUAL(student, reference)                                                    \
    do {                                                                                    \
       auto _studentAnswer   = (student);                                                   \
       auto _referenceAnswer = (reference);                                                 \
                                                                                            \
       std::stringstream _expression;                                                       \
       _expression << std::boolalpha << "EXPECT_EQUAL failed: "                             \
                   << #student << " != " << #reference "\n"                                 \
                   << "                " #student   " = "                                   \
                   << abbreviate(debugFriendlyString(_studentAnswer)) << '\n'                           \
                   << "                " #reference " = "                                   \
                   << abbreviate(debugFriendlyString(_referenceAnswer));                                \
       doExpect(_areEqual(_studentAnswer, _referenceAnswer), _expression.str(), __LINE__); \
    } while (0)

#undef REPORT_FAILURE
#define REPORT_FAILURE(message) doFail(message, __LINE__)

#undef TIME_OPERATION
#define TIME_OPERATION(n, expr) do {\
    Timer t;\
    t.start();\
    (void)(expr); \
    double elapsed = t.stop();\
    ostringstream _out; \
    _out << "Line " << __LINE__ << " Time " << #expr << " (size =" << setw(7) << n << ")" << " completed in " << setw(8) << (elapsed/1000) << " secs";\
    addDetail(_out.str());\
} while(0)
