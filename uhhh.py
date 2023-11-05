import streamlit as st
import pandas as pd

def fadd(a, b, carry_in):
    sum_ab = int(a) + int(b) + int(carry_in)
    sum_out = str(sum_ab % 2)
    carry_out = str(sum_ab // 2)
    return sum_out, carry_out

def add(a, b):
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    carry = "0"
    result = ""
    for i in range(max_len - 1, -1, -1):
        sum_out, carry = fadd(a[i], b[i], carry)
        result = sum_out + result

    result = list(result)
    carry = list(carry)
    for i in range(len(result)):
        carry.append(result[i])

    temp = []
    for i in range(len(result) + 1):
        if i == 0:
            pass
        else:
            temp.append(carry[i])
    temp = "".join(temp)
    return temp

def twoscomplement(m):
    m = list(m)
    for i in range(len(m) - 1, -1, -1):
        if m[i] == "0":
            m[i] = "1"
        elif m[i] == "1":
            m[i] = "0"
    m = "".join(m)
    ans = add(m, "1")
    ans = "".join(ans)
    return ans

def right_shift(acc, q, q0):
    acc = list(acc)
    q = list(q)
    temp1 = acc[len(acc) - 1]
    q0 = q[len(q) - 1]

    for i in range(len(acc) - 1, 0, -1):
        acc[i] = acc[i - 1]

    for i in range(len(q) - 1, 0, -1):
        q[i] = q[i - 1]
    q[0] = temp1
    acc = "".join(acc)
    q = "".join(q)
    q0 = "".join(q0)
    return acc, q, q0

def boothmultiplication(x, y):
    x_bin = bin(int(x))[2:]
    y_bin = bin(int(y))[2:]
    n = max(len(x_bin), len(y_bin)) + 1
    x_bin = x_bin.zfill(n)
    y_bin = y_bin.zfill(n)
    a = 0
    acc = f"{a:0{n}b}"
    q = y_bin
    q0 = "0"
    
    steps = []
    
    for i in range(n, 0, -1):
        lsb = int(q) & 1
        comp = str(lsb) + q0
        if (comp == "00" or comp == "11"):
            acc, q, q0 = right_shift(acc, q, q0)
            steps.append((i, acc, q, q0, "Arithmetic Right Shift"))
        elif (comp == "01"):
            acc = add(acc, x_bin)
            acc, q, q0 = right_shift(acc, q, q0)
            steps.append((i, acc, q, q0, "A<-A+M and Arithmetic Right Shift"))
        elif (comp == "10"):
            xcomp = twoscomplement(x_bin)
            acc = add(acc, xcomp)
            acc, q, q0 = right_shift(acc, q, q0)
            steps.append((i, acc, q, q0, "A<-A-M and Arithmetic Right Shift"))
    
    result = acc + q
    result = int(result, 2)
    
    st.write(f"Booth Multiplication of {x} and {y}")
    st.write(pd.DataFrame(steps, columns=["Count", "A", "Q", "Q0", "Operation"]))
    st.write(f"Product: {result}")
    return result

def main():
    data = []
    
    st.title("Daily Spending and Budget Assessment")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    columns = [col1,col2,col3,col4,col5,col6,col7]

    for i in range(7):
        day = f"Day {i + 1}"

        with columns[i]:
            st.header(day)
            Travel = st.number_input("Travel amount", key=f"travel_{i}",value=0)
            Food = st.number_input("Food amount", key=f"food_{i}",value=0)
            Network = st.number_input("Network Bill amount", key=f"network_{i}",value=0)
            Shopping = st.number_input("Shopping amount", key=f"shopping_{i}",value=0)

            total = Travel + Food + Network + Shopping
            total = int(total)
            binary_total = bin(total)
            data.append([day, Travel, Food, Network, Shopping, total, binary_total])
    
    st.write("Weekly Spending Data")
    st.write(data)
    
    total_weekly_spending = sum(row[5] for row in data)
    binary_total_weekly_spending = bin(total_weekly_spending)
    
    st.write("\nTotal Weekly Spending:", total_weekly_spending)

    y = st.number_input("Enter the multiplier (for booth multiplication)", value=4)

        

    Bud = st.number_input("Enter your Budget",value=0)
    if st.button("Check Budget"):
        result = boothmultiplication(total_weekly_spending, y)
        st.write(f"Result of {total_weekly_spending} * {y} is {result}")
        save = Bud - result
        if save > 0:
            st.write("You are under Budget")
        elif save < 0:
            st.write("You are over Budget")
        elif save == 0:
            st.write("You are equal to Budget")

if __name__ == '__main__':
    main()
