#include <ldap.h>
#include <stdio.h>
int
main(int argc, char **argv)
{
	printf("%d\n", LDAP_VENDOR_VERSION);
	return 0;
}
