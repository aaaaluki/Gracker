#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

void spawn_shell() {
    gid_t gid;
    uid_t uid;
    gid = getegid();
    uid = geteuid();
    setresgid(gid, gid, gid);
    setresuid(uid, uid, uid);
    system("/bin/sh");
}

int main(int argc, char **argv)
{
  volatile int admin_enabled;
  char buffer[64];
  admin_enabled = 0;

  printf("Zero Cool - Bugdoor v4\nEnter Password:\n");
  gets(buffer);

  if(admin_enabled != 0) {
      printf("How can this happen? The variable is set to 0 and is never modified in between O.o\nYou must be a hacker!\n");
      spawn_shell();
  } else {
      printf("Trololol lololol...\n");
  }
}
