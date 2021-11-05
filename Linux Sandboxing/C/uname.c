#include <stdio.h>
#include <sys/utsname.h>

int main(void)
{
    struct utsname name;

    if (uname(&name)) {
        perror("uname failed: ");
        return 1;
    }

    printf("My OS is %s!\n", name.sysname);
    return 0;
}
