# 집합 A = {1, 2, 3, 4, 5}
n = 5


# -입력
def inputMat():
    print(f"집합 A = {{1, 2, 3, 4, 5}} 에 관한 {n} x {n} 관계행렬을 행 단위로 입력하세요. (0 또는 1, 공백으로 구분)")
    mat = []
    for i in range(n):
        while True:
            try:
                row = [int(x) for x in input(f"{i + 1}행: ").split()]
            except ValueError:
                print("입력 오류: 숫자만 입력하세요.")
                continue
            if len(row) != n:
                print(f"입력 오류: 정확히 {n}개의 값을 입력해야 합니다.")
                continue
            if any(v not in (0, 1) for v in row):
                print("입력 오류: 0 또는 1만 입력하세요.")
                continue
            mat.append(row)
            break
    return mat


def printMat(mat):
    for row in mat:
        print(row)
    print()


# 추가기능 : 곱집합 크기 공식 이용
def countRel(mat):
    count = 0
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 1:
                count += 1
    return count



# 반사관계
def isRef(mat):
    for i in range(n):
        if mat[i][i] != 1:
            return False
    return True


# 대칭관계
def isSym(mat):
    for i in range(n):
        for j in range(n):
            if mat[i][j] != mat[j][i]:
                return False
    return True 

# 부울곱
def boolMul(a, b):
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if a[i][k] == 1 and b[k][j] == 1:
                    result[i][j] = 1
    return result


# 추이관계 
def isTra(mat):
    power = [row[:] for row in mat]    
    for k in range(2, n + 1):
        power = boolMul(power, mat)  
        for i in range(n):
            for j in range(n):
                if power[i][j] == 1 and mat[i][j] == 0:
                    return False
    return True


# 반사, 대칭, 추이 결과
def checkEqu(mat):
    r = isRef(mat)
    s = isSym(mat)
    t = isTra(mat)
    print("반사관계 :", "O" if r else "X")
    print("대칭관계 :", "O" if s else "X")
    print("추이관계 :", "O" if t else "X")
    if r and s and t:
        print("=> 반사, 대칭, 추이관계를 모두 만족하므로 동치관계입니다.")
    else:
        print("=> 동치관계가 아닙니다.")
    print()
    return r, s, t

# 동치류
def equivalenceCla(mat, a):
    return [x + 1 for x in range(n) if mat[a - 1][x] == 1]


def printEquCla(mat):
    for a in range(1, n + 1): 
        print(f"[{a}] = {equivalenceCla(mat, a)}")
    print()


# 반사폐포
def reflexiveClo(mat):
    s = [row[:] for row in mat]
    for i in range(n):
        s[i][i] = 1 
    return s


# 대칭폐포
def symmetricClo(mat):
    s = [row[:] for row in mat]
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 1:
                s[j][i] = 1 
    return s


# 추이폐포 
def transitiveClo(mat): 
    w = [row[:] for row in mat] 
    for k in range(n):
        for i in range(n):
            for j in range(n): 
                if w[i][j] == 0 and w[i][k] == 1 and w[k][j] == 1:
                    w[i][j] = 1
    return w


# 폐포로 변환
def makeClo(mat, r, s, t):
    result = [row[:] for row in mat]
    if not r:
        print("=== 반사폐포로 변환 ===")
        print("변환 전:")
        printMat(result)
        result = reflexiveClo(result)
        print("변환 후:")
        printMat(result)
    if not s:
        print("=== 대칭폐포로 변환 ===")
        print("변환 전:")
        printMat(result)
        result = symmetricClo(result)
        print("변환 후:")
        printMat(result)
    if not t or not isTra(result):
        print("=== 추이폐포로 변환 (와샬 알고리즘) ===")
        print("변환 전:")
        printMat(result)
        result = transitiveClo(result)
        print("변환 후:")
        printMat(result)
    return result


def main():
    matrix = inputMat()

    print("\n입력한 관계 행렬:")
    printMat(matrix)
    size_r = countRel(matrix)
    print(f"|A×A| = |A| × |A| = {n} × {n} = {n * n}")
    print(f"|R| = {size_r}  (A×A의 원소 {n * n}개 중 {size_r}개가 R에 속함)\n")

    print("[동치관계 판별]")
    r, s, t = checkEqu(matrix)

    if r and s and t:
        print("[동치류]")
        printEquCla(matrix)
    else:
        print("[폐포 변환]")
        new_matrix = makeClo(matrix, r, s, t)

        size_s = countRel(new_matrix)
        print(f"폐포 변환 후 |S| = {size_s}  (|S| - |R| = {size_s - size_r}개 증가)\n")

        print("[폐포 변환 후 동치관계 재판별]")
        r, s, t = checkEqu(new_matrix)
        if r and s and t:
            print("[동치류]")
            printEquCla(new_matrix)


main()
