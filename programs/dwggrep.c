/*****************************************************************************/
/*  LibreDWG - free implementation of the DWG file format                    */
/*                                                                           */
/*  Copyright (C) 2018 Free Software Foundation, Inc.                        */
/*                                                                           */
/*  This library is free software, licensed under the terms of the GNU       */
/*  General Public License as published by the Free Software Foundation,     */
/*  either version 3 of the License, or (at your option) any later version.  */
/*  You should have received a copy of the GNU General Public License        */
/*  along with this program.  If not, see <http://www.gnu.org/licenses/>.    */
/*****************************************************************************/

/*
 * dwggrep.c: search a string in all text values in a DWG
 * TODO scan the dwg.spec for all text DXF codes, per object.
 * uses pcre2-8 (not yet pcre2-16, rather convert down to UTF-8)
 *
 * written by Reini Urban
 */

#include "../src/config.h"
#include <stdio.h>
#include <stdlib.h>
#ifdef HAVE_STRCASESTR
# undef  __DARWIN_C_LEVEL
# define __DARWIN_C_LEVEL __DARWIN_C_FULL
# include <string.h>
#else
# include <string.h>
# include <ctype.h>
#endif
#ifdef HAVE_PCRE2_H
# define PCRE2_CODE_UNIT_WIDTH 8
# include <pcre2.h>
//Maybe: for r2007+ use pcre2-16, before use pcre2-8
//       Currently we convert to UTF-8
#endif

#include "dwg.h"
#include "../src/logging.h"
#include "../src/common.h"
#include "../src/bits.h"
#include "suffix.inc"
static int help(void);
int verbosity(int argc, char **argv, int i, unsigned int *opts);
#include "common.inc"
#include "dwg_api.h"

#ifndef HAVE_PCRE2_H
# define PCRE2_DUPNAMES 0
# define PCRE2_CASELESS 1
# define PCRE2_EXTENDED 2
#endif

char *pattern;
char buf[4096];
int options = PCRE2_DUPNAMES;
int opt_count = 0;

/* the current version per spec block */
static unsigned int cur_ver = 0;

#ifdef HAVE_PCRE2_H
# undef USE_MATCH_CONTEXT
/* pcre2_compile */
static pcre2_code_8 *ri;
static pcre2_match_data_8 *match_data;
static pcre2_match_context_8 *match_context = NULL;

# ifdef USE_MATCH_CONTEXT
static pcre2_jit_stack *jit_stack = NULL;
static pcre2_compile_context_8 *compile_context = NULL;
# endif
# define PUBLIC_JIT_MATCH_OPTIONS \
   (PCRE2_NO_UTF_CHECK|PCRE2_NOTBOL|PCRE2_NOTEOL|PCRE2_NOTEMPTY|\
    PCRE2_NOTEMPTY_ATSTART|PCRE2_PARTIAL_SOFT|PCRE2_PARTIAL_HARD)
#endif

static int usage(void) {
  printf("\nUsage: dwggrep [-cRr] pattern *.dwg\n");
  return 1;
}
static int opt_version(void) {
  printf("dwggrep %s\n", PACKAGE_VERSION);
  return 0;
}
static int help(void) {
  printf("\nUsage: dwggrep [OPTIONS]... pattern files\n");
#ifdef HAVE_PCRE2_H
  printf("Search regex pattern in a list of DWGs.\n\n");
#else
  printf("Search string (no regex) in a list of DWGs.\n\n");
#endif
  printf("  -i                        Case-insensitive pattern\n");
#ifdef HAVE_PCRE2_H
  printf("  -x                        Extended regex pattern\n");
#endif
#if 0
  printf("  --type NAME               Search only NAME entities or objects.\n");
  printf("  --dxf NUM                 Search only DXF group NUM fields.\n");
  // for now only this:
  printf("  --text                    Search only in TEXT-like entities.\n");
  printf("  --tables                  Search only in table names.\n");
  printf("  -R, -r, --recursive       Recursively search subdirectories listed.\n");
#endif
  printf("  -c, --count               Print only the count of matched elements.\n");
  printf("      --help                Display this help and exit\n");
  printf("      --version             Output version information and exit\n"
         "\n");
  printf("GNU LibreDWG online manual: <https://www.gnu.org/software/libredwg/>\n");
  return 0;
}

static int
do_match (char *filename, char *entity, int dxf, char* text, int textlen)
{
#ifdef HAVE_PCRE2_H
  int found = pcre2_jit_match_8(ri, (PCRE2_SPTR8)text, textlen, 0,
                                PUBLIC_JIT_MATCH_OPTIONS,
                                match_data,     /* block for storing the result */
                                match_context); /* disabled */
  if (found >= 0) {
    if (!opt_count)
      printf("%s %s %d: %s\n", filename, entity, dxf, text);
    return 1;
  }
#else
  if (options & PCRE2_CASELESS)
    {
# ifndef HAVE_STRCASESTR
      int i, len;
      char *dest = text;
      int dlen = textlen;
      char *src = pattern;
      int slen = strlen(pattern);
      while (*dest && dlen)
        {
          i = 0;
          len = slen;
          dlen = textlen;
          if (toupper((unsigned char)dest[i]) != toupper((unsigned char)src[i])) {
            break;
          }
          /* move to the next char */
          i++;
          len--;
          dlen--;

          if (src[i] == '\0' || !len) {
            if (!opt_count)
              printf("%s %s %d: %s\n", filename, entity, dxf, text);
            return 1;
          }
          dest++;
        }
# else
      if (strcasestr(text, pattern))
        {
          if (!opt_count)
            printf("%s %s %d: %s\n", filename, entity, dxf, text);
          return 1;
        }
# endif
    }
  else
    {
      if (strstr(text, pattern)) {
        if (!opt_count)
          printf("%s %s %d: %s\n", filename, entity, dxf, text);
        return 1;
      }
    }
#endif
  return 0;
}
  
static
int match_TEXT(char* filename, Dwg_Object* obj)
{
  char *text = obj->tio.entity->tio.TEXT->text_value;
  int found, textlen;
  if (obj->parent->header.version >= R_2007)
    text = bit_convert_TU((BITCODE_TU)text);
  textlen = strlen(text);

  found = do_match(filename, "TEXT", 1, text, textlen);

  if (obj->parent->header.version >= R_2007)
    free(text);
  return found;
}

static
int match_ATTRIB(char* filename, Dwg_Object* obj)
{
  char *text = obj->tio.entity->tio.ATTRIB->text_value;
  int found, textlen;
  if (obj->parent->header.version >= R_2007)
    text = bit_convert_TU((BITCODE_TU)text);
  textlen = strlen(text);

  found = do_match(filename, "ATTRIB", 1, text, textlen);

  if (obj->parent->header.version >= R_2007)
    free(text);
  return found;
}

static
int match_MTEXT(char* filename, Dwg_Object* obj)
{
  char *text = obj->tio.entity->tio.MTEXT->text;
  int found, textlen;
  if (obj->parent->header.version >= R_2007)
    text = bit_convert_TU((BITCODE_TU)text);
  textlen = strlen(text);

  found = do_match(filename, "MTEXT", 1, text, textlen);

  if (obj->parent->header.version >= R_2007)
    free(text);
  return found;
}

static
int match_BLOCK_HEADER(char* filename, Dwg_Object_Ref* ref)
{
  int found = 0;
  Dwg_Object* obj;
  //Dwg_Object_BLOCK_HEADER* hdr;

  if (!ref || !ref->obj || !ref->obj->tio.object)
    return 0;
  //hdr = ref->obj->tio.object->tio.BLOCK_HEADER;
  obj = get_first_owned_object(ref->obj);
  while (obj)
    {
      if (obj->type == DWG_TYPE_TEXT)
        found += match_TEXT(filename, obj);
      else if (obj->type == DWG_TYPE_ATTRIB)
        found += match_ATTRIB(filename, obj);
      else if (obj->type == DWG_TYPE_MTEXT)
        found += match_MTEXT(filename, obj);
      obj = get_next_owned_object(ref->obj, obj);
    }
  return found;
}

int
main (int argc, char *argv[])
{
  int error = 0;
  int i = 1, j;
  char* filename;
  Dwg_Data dwg;
  Bit_Chain dat;
  short dxf[10];
  char* objtype[10];
  short numdxf = 0;
  short numtype = 0;
  int plen;
  int errcode;
#ifdef HAVE_PCRE2_H
  PCRE2_SIZE erroffset;
  /* pcre_compile */
  int have_jit;
#endif
  int count = 0;

  // check args
  if (argc < 2)
    return usage();

  memset(dxf, 0, 10*sizeof(short));
  if (i < argc && !strcmp(argv[i], "-i"))
    {
      options |= PCRE2_CASELESS;
      i++;
    }
#ifdef HAVE_PCRE2_H
  if (i < argc && !strcmp(argv[i], "-x"))
    {
      options |= PCRE2_EXTENDED;
      i++;
    }
#endif
  if (i < argc-1 && !strcmp(argv[i], "--type"))
    {
      if (numtype>=10) exit(1);
      objtype[numtype++] = argv[i+1];
      i += 2;
    }
  if (i < argc-1 && !strcmp(argv[i], "--dxf"))
    {
      if (numdxf>=10) exit(1);
      dxf[numdxf++] = (short)strtol(argv[i+1], NULL, 10);
      i += 2;
    }
  if (i < argc && (!strcmp(argv[i], "--count") || !strcmp(argv[i], "-c")))
    {
      opt_count = 1;
      i++;
    }
  if (i < argc && !strcmp(argv[i], "--help"))
    return help();
  if (i < argc && !strcmp(argv[i], "--version"))
    return opt_version();

  if (i > argc-2) // need 2 more args. TODO: unless -R given
    return usage();

  pattern = argv[i]; plen = strlen(pattern);
#ifdef HAVE_PCRE2_H
  pcre2_config_8(PCRE2_CONFIG_JIT, &have_jit);
  ri = pcre2_compile_8(
     (PCRE2_SPTR8)pattern, plen, /* pattern */
     options,      /* options */
     &errcode,     /* errors */
     &erroffset,   /* error offset */
# ifdef USE_MATCH_CONTEXT
     compile_context
# else
     NULL
# endif
    );
  match_data = pcre2_match_data_create_from_pattern_8(ri, NULL);
  pcre2_jit_compile_8(ri, PCRE2_JIT_COMPLETE); /* no partial matches */
#endif

  //for all filenames...
  for (j=i+1; j<argc; j++)
    {
      long k;

      filename = argv[j];
      memset(&dwg, 0, sizeof(Dwg_Data));
      dwg.opts = 0;
      error = dwg_read_file(filename, &dwg);
      if (error > DWG_ERR_CRITICAL)
        {
          fprintf(stderr, "Error: Could not read DWG file %s, error: 0x%x\n",
                  filename, error);
          continue;
        }

      for (k=0; k < dwg.block_control.num_entries; k++)
        {
          count += match_BLOCK_HEADER(filename, dwg.block_control.block_headers[k]);
        }
      count += match_BLOCK_HEADER(filename, dwg.block_control.model_space);
      count += match_BLOCK_HEADER(filename, dwg.block_control.paper_space);

      if (j < argc)
        dwg_free(&dwg); //skip the last free
    }
  if (opt_count)
    printf("%d\n", count);

  return count ? 0 : 1;
}