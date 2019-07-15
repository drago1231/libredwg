/* -*- c -*- */
/*****************************************************************************/
/*  LibreDWG - free implementation of the DWG file format                    */
/*                                                                           */
/*  Copyright (C) 2018-2019 Free Software Foundation, Inc.                   */
/*                                                                           */
/*  This library is free software, licensed under the terms of the GNU       */
/*  General Public License as published by the Free Software Foundation,     */
/*  either version 3 of the License, or (at your option) any later version.  */
/*  You should have received a copy of the GNU General Public License        */
/*  along with this program.  If not, see <http://www.gnu.org/licenses/>.    */
/*****************************************************************************/

/*
 * header_variables_dxf.spec: DXF header variables specification
 * written by Reini Urban
 */

//TODO: SINCE(R_2010): LASTSAVEDBY, 1, ""

#include "spec.h"

  SECTION(HEADER);

  HEADER_VALUE (ACADVER, TV, 1, version_codes[dwg->header.version]);

  if (minimal) {
    HEADER_VALUE (HANDSEED, RS, 5, _obj->HANDSEED->absolute_ref);
    ENDSEC();
    return 0;
  }

  VERSIONS(R_13, R_2013) {
    HEADER_VALUE (ACADMAINTVER, RC, 70, dwg->header.maint_version);
  }
  SINCE(R_2018) {
    HEADER_VALUE (ACADMAINTVER, RC, 90, dwg->header.maint_version);
  }
  SINCE(R_10) {
    HEADER_VALUE (DWGCODEPAGE, TV, 3, codepage);
  }
  SINCE(R_2010) {
    HEADER_TU (LASTSAVEDBY, 1);
    //HEADER_VALUE (LASTSAVEDBY, TU, 1, "");
  }
  SINCE(R_2013) {
    HEADER_BLL (REQUIREDVERSIONS, 160);
  }
  HEADER_3D (INSBASE);
  HEADER_3D (EXTMIN);
  HEADER_3D (EXTMAX);
  HEADER_2D (LIMMIN);
  HEADER_2D (LIMMAX);

  HEADER_RC (ORTHOMODE, 70);
  HEADER_RC (REGENMODE, 70);
  HEADER_RC (FILLMODE, 70);
  HEADER_RC (QTEXTMODE, 70);
  HEADER_RC (MIRRTEXT, 70);
  UNTIL(R_14) {
    HEADER_RC (DRAGMODE, 70);
  }
  HEADER_RD (LTSCALE, 40);
  UNTIL(R_14) {
    HEADER_RC (OSMODE, 70);
  }
  HEADER_RC (ATTMODE, 70);
  HEADER_RD (TEXTSIZE, 40);
  HEADER_RD (TRACEWID, 40);

  HEADER_HANDLE_NAME (TEXTSTYLE, 7, STYLE);
  HEADER_HANDLE_NAME (CLAYER, 8, LAYER);
  HEADER_HANDLE_NAME (CELTYPE, 6, LTYPE);
  HEADER_CMC (CECOLOR, 62);
  SINCE(R_13) {
    HEADER_RD (CELTSCALE, 40);
    UNTIL(R_14) {
      HEADER_RC (DELOBJ, 70);
    }
    HEADER_RC (DISPSILH, 70); // this is WIREFRAME
    HEADER_RD (DIMSCALE, 40);
  }
  HEADER_RD (DIMASZ, 40);
  HEADER_RD (DIMEXO, 40);
  HEADER_RD (DIMDLI, 40);
  HEADER_RD (DIMRND, 40);
  HEADER_RD (DIMDLE, 40);
  HEADER_RD (DIMEXE, 40);
  HEADER_RD (DIMTP, 40);
  HEADER_RD (DIMTM, 40);
  HEADER_RD (DIMTXT, 40);
  HEADER_RD (DIMCEN, 40);
  HEADER_RD (DIMTSZ, 40);
  HEADER_RC (DIMTOL, 70);
  HEADER_RC (DIMLIM, 70);
  HEADER_RC (DIMTIH, 70);
  HEADER_RC (DIMTOH, 70);
  HEADER_RC (DIMSE1, 70);
  HEADER_RC (DIMSE2, 70);
  HEADER_RC (DIMTAD, 70);
  HEADER_RC (DIMZIN, 70);
  HEADER_HANDLE_NAME (DIMBLK, 1, BLOCK_HEADER);
  HEADER_RC (DIMASO, 70);
  HEADER_RC (DIMSHO, 70);
  PRE(R_14) {
    HEADER_RC (DIMSAV, 70);
  }
  HEADER_TV (DIMPOST, 1);
  HEADER_TV (DIMAPOST, 1);
  HEADER_RC (DIMALT, 70);
  HEADER_RC (DIMALTD, 70);
  HEADER_RD (DIMALTF, 40);
  HEADER_RD (DIMLFAC, 40);
  HEADER_RC (DIMTOFL, 70);
  HEADER_RD (DIMTVP, 40);
  HEADER_RC (DIMTIX, 70);
  HEADER_RC (DIMSOXD, 70);
  HEADER_RC (DIMSAH, 70);
  HEADER_HANDLE_NAME (DIMBLK1, 1,  BLOCK_HEADER);
  HEADER_HANDLE_NAME (DIMBLK2, 1,  BLOCK_HEADER);
  HEADER_HANDLE_NAME (DIMSTYLE, 2, DIMSTYLE);
  HEADER_CMC (DIMCLRD, 70);
  HEADER_CMC (DIMCLRE, 70);
  HEADER_CMC (DIMCLRT, 70);
  HEADER_RD (DIMTFAC, 40);
  HEADER_RD (DIMGAP, 40);
  SINCE(R_13) {
    HEADER_RC (DIMJUST, 70);
    HEADER_RC (DIMSD1, 70);
    HEADER_RC (DIMSD2, 70);
    HEADER_RC (DIMTOLJ, 70);
    HEADER_RC (DIMTZIN, 70);
    HEADER_RC (DIMALTZ, 70);
    HEADER_RC (DIMALTTZ, 70);
    HEADER_RC (DIMFIT, 70);  //optional
    HEADER_RC (DIMUPT, 70);
    HEADER_RC (DIMUNIT, 70); //optional
    HEADER_RC (DIMDEC, 70);
    HEADER_RC (DIMTDEC, 70);
    HEADER_RC (DIMALTU, 70);
    HEADER_RC (DIMALTTD, 70);
    HEADER_HANDLE_NAME (DIMTXSTY, 7, STYLE);
    HEADER_RC (DIMAUNIT, 70);
  }
  SINCE(R_2000) {
    HEADER_RC (DIMADEC, 70);
    HEADER_RD (DIMALTRND, 40);
    HEADER_RC (DIMAZIN, 70);
    HEADER_RC (DIMDSEP, 70);
    HEADER_RC (DIMATFIT, 70);
    HEADER_RC (DIMFRAC, 70);
    HEADER_HANDLE_NAME (DIMLDRBLK, 1, BLOCK_HEADER);
    HEADER_RC (DIMLUNIT, 70);
    //HEADER_RC (DIMLWD, 70); convert from unsigned to signed
    //HEADER_RC (DIMLWE, 70);
    HEADER_VALUE (DIMLWD, RS, 70, (int16_t)_obj->DIMLWD);
    HEADER_VALUE (DIMLWE, RS, 70, (int16_t)_obj->DIMLWE);
    HEADER_RC (DIMTMOVE, 70);
  }
  SINCE(R_2007)
    {
      HEADER_BD (DIMFXL, 40);
      HEADER_B (DIMFXLON, 70);
      HEADER_BD (DIMJOGANG, 40);
      HEADER_BS (DIMTFILL, 70);
      HEADER_CMC (DIMTFILLCLR, 70);
      HEADER_BS (DIMARCSYM, 70);
      HEADER_HANDLE_NAME (DIMLTYPE, 6, LTYPE);
      HEADER_HANDLE_NAME (DIMLTEX1, 6, LTYPE);
      HEADER_HANDLE_NAME (DIMLTEX2, 6, LTYPE);
    }
  SINCE(R_2010)
    {
      HEADER_B (DIMTXTDIRECTION, 70);
    }
  HEADER_RC (LUNITS, 70);
  HEADER_RC (LUPREC, 70);
  HEADER_RD (SKETCHINC, 40);
  HEADER_RD (FILLETRAD, 40);
  HEADER_RC (AUNITS, 70);
  HEADER_RC (AUPREC, 70);
  HEADER_TV (MENU, 1);
  HEADER_RD (ELEVATION, 40);
  HEADER_RD (PELEVATION, 40);
  HEADER_RD (THICKNESS, 40);
  HEADER_RC (LIMCHECK, 70);
  UNTIL(R_14) {
    //HEADER_RC (BLIPMODE, 70); //documented but nowhere found
  }
  HEADER_RD (CHAMFERA, 40);
  HEADER_RD (CHAMFERB, 40);
  SINCE(R_13) {
    HEADER_RD (CHAMFERC, 40);
    HEADER_RD (CHAMFERD, 40);
  }
  HEADER_RC (SKPOLY, 70);

  HEADER_TIMEBLL (TDCREATE, 40);
  /*SINCE(R_13) {
    HEADER_TIMEBLL (TDUCREATE, 40);
  }*/
  HEADER_TIMEBLL (TDUPDATE, 40);
  /*SINCE(R_13) {
    HEADER_TIMEBLL (TDUUPDATE, 40);
  }*/
  HEADER_TIMEBLL (TDINDWG, 40);
  HEADER_TIMEBLL (TDUSRTIMER, 40);

  HEADER_VALUE (USRTIMER, RC, 70, 1); // 1
  HEADER_RD (ANGBASE, 50);
  HEADER_RC (ANGDIR, 70);
  HEADER_RC (PDMODE, 70);
  HEADER_RD (PDSIZE, 40);
  HEADER_RD (PLINEWID, 40);
  UNTIL(R_14) {
    HEADER_RC (COORDS, 70); // 2
  }
  HEADER_RC (SPLFRAME, 70);
  HEADER_RC (SPLINETYPE, 70);
  HEADER_RC (SPLINESEGS, 70);
  UNTIL(R_14) {
    HEADER_RC (ATTDIA, 70); //default 1
    HEADER_RC (ATTREQ, 70); //default 1
    HEADER_RC (HANDLING, 70); //default 1
  }

  //HEADER_VALUE (HANDSEED, RS, 5, _obj->HANDSEED->absolute_ref);
  HEADER_H (HANDSEED, 5); //default: 20000, before r13: 0xB8BC

  HEADER_RC (SURFTAB1, 70); // 6
  HEADER_RC (SURFTAB2, 70); // 6
  HEADER_RC (SURFTYPE, 70); // 6
  HEADER_RC (SURFU, 70); // 6
  HEADER_RC (SURFV, 70); // 6
  SINCE(R_2000) {
    HEADER_HANDLE_NAME (UCSBASE, 2, UCS);
  }
  HEADER_HANDLE_NAME (UCSNAME, 2, UCS);
  HEADER_3D (UCSORG);
  HEADER_3D (UCSXDIR);
  HEADER_3D (UCSYDIR);
  SINCE(R_2000) {
    HEADER_HANDLE_NAME (UCSORTHOREF, 2, UCS);
    HEADER_RC (UCSORTHOVIEW, 70);
    HEADER_3D (UCSORGTOP);
    HEADER_3D (UCSORGBOTTOM);
    HEADER_3D (UCSORGLEFT);
    HEADER_3D (UCSORGRIGHT);
    HEADER_3D (UCSORGFRONT);
    HEADER_3D (UCSORGBACK);
    HEADER_HANDLE_NAME (PUCSBASE, 2, UCS);
  }
  HEADER_HANDLE_NAME (PUCSNAME, 2, UCS);
  HEADER_3D (PUCSORG);
  HEADER_3D (PUCSXDIR);
  HEADER_3D (PUCSYDIR);
  SINCE(R_2000) {
    HEADER_HANDLE_NAME (PUCSORTHOREF, 2, UCS);
    HEADER_RC (PUCSORTHOVIEW, 70);
    HEADER_3D (PUCSORGTOP);
    HEADER_3D (PUCSORGBOTTOM);
    HEADER_3D (PUCSORGLEFT);
    HEADER_3D (PUCSORGRIGHT);
    HEADER_3D (PUCSORGFRONT);
    HEADER_3D (PUCSORGBACK);
  }

  HEADER_RC (USERI1, 70);
  HEADER_RC (USERI2, 70);
  HEADER_RC (USERI3, 70);
  HEADER_RC (USERI4, 70);
  HEADER_RC (USERI5, 70);
  HEADER_RD (USERR1, 40);
  HEADER_RD (USERR2, 40);
  HEADER_RD (USERR3, 40);
  HEADER_RD (USERR4, 40);
  HEADER_RD (USERR5, 40);

  HEADER_RC (WORLDVIEW, 70);
  //VERSION(R_13) {
  //  HEADER_RC (WIREFRAME, 70); //Undocumented
  //}
  HEADER_RC (SHADEDGE, 70);
  HEADER_RC (SHADEDIF, 70);
  HEADER_RC (TILEMODE, 70);
  HEADER_RC (MAXACTVP, 70);

  HEADER_3D (PINSBASE);
  HEADER_RC (PLIMCHECK, 70);
  HEADER_3D (PEXTMIN);
  HEADER_3D (PEXTMAX);
  HEADER_2D (PLIMMIN);
  HEADER_2D (PLIMMAX);

  HEADER_RC (UNITMODE, 70);
  HEADER_RC (VISRETAIN, 70);
  VERSION(R_13) {
    HEADER_RC (DELOBJ, 70);
  }
  HEADER_RC (PLINEGEN, 70);
  HEADER_RC (PSLTSCALE, 70);
  HEADER_RC (TREEDEPTH, 70);
  UNTIL(R_11) {
    HEADER_VALUE (DWGCODEPAGE, TV, 3, codepage);
  }
  VERSIONS(R_14, R_2000) { //? maybe only for r14
    HEADER_RC (PICKSTYLE, 70);
  }
  HEADER_HANDLE_NAME (CMLSTYLE, 2, MLINESTYLE); //default: Standard
  HEADER_RC (CMLJUST, 70);
  HEADER_RD (CMLSCALE, 40); //default: 20
  VERSION(R_13) {
    HEADER_RC (SAVEIMAGES, 70);
  }
  SINCE(R_14) {
    HEADER_RC (PROXYGRAPHICS, 70);
  }
  HEADER_VALUE (MEASUREMENT, RC, 70,
                dwg->header.num_sections > SECTION_MEASUREMENT_R13 ? 1 : 0);
  SINCE(R_2000) {
    PRINT {
      HEADER_9(CELWEIGHT);
      VALUE(dxf_cvt_lweight(_obj->CELWEIGHT), RCs, 370);
    }
    ENCODER {
      // TODO reverse lookup
      HEADER_RC (CELWEIGHT, 370);
    }

    HEADER_RC (ENDCAPS, 280);
    HEADER_RC (JOINSTYLE, 280);
    HEADER_B (LWDISPLAY, 290);
    HEADER_RC (INSUNITS, 70);
    HEADER_TV (HYPERLINKBASE, 1);
    HEADER_TV (STYLESHEET, 1);
    HEADER_B (XEDIT, 290);
    HEADER_RC (CEPSNTYPE, 380);

    if (dwg->header_vars.CEPSNTYPE == 3)
    {
      HEADER_HANDLE_NAME (CPSNID, 390, LTYPE);
    }
    HEADER_B (PSTYLEMODE, 290);
    HEADER_T (FINGERPRINTGUID, 2);
    HEADER_T (VERSIONGUID, 2);
    HEADER_B (EXTNAMES, 290);
    HEADER_RD (PSVPSCALE, 40);
    HEADER_B (OLESTARTUP, 290);
  }

  SINCE(R_2004)
    {
      HEADER_RC (SORTENTS, 280);
      HEADER_RC (INDEXCTL, 280);
      HEADER_RC (HIDETEXT, 280);
      SINCE(R_2007) {
        HEADER_RC (XCLIPFRAME, 280);
      } else {
        HEADER_B (XCLIPFRAME, 290);
      }
      PRE(R_2007) {
        HEADER_RC (DIMASSOC, 280);
      }
      HEADER_RC (HALOGAP, 280);
      HEADER_BS (OBSCOLOR, 70);
      HEADER_RC (OBSLTYPE, 280);
      HEADER_RC (INTERSECTIONDISPLAY, 280);
      HEADER_BS (INTERSECTIONCOLOR, 70);
      SINCE(R_2007) {
        HEADER_RC (DIMASSOC, 280);
      }
      HEADER_T (PROJECTNAME, 1);
    }

  SINCE(R_2007)
    {
      HEADER_B (CAMERADISPLAY, 290);
      HEADER_BD (LENSLENGTH, 40);
      HEADER_BD (CAMERAHEIGHT, 40);
      HEADER_BD (STEPSPERSEC, 40);
      HEADER_BD (STEPSIZE, 40);
      HEADER_VALUE (3DDWFPREC, BD, 40, _obj->_3DDWFPREC);
      HEADER_BD (PSOLWIDTH, 40);
      HEADER_BD (PSOLHEIGHT, 40);
      HEADER_BD (LOFTANG1, 40); //no rad2deg, ok
      HEADER_BD (LOFTANG2, 40); //no rad2deg, ok
      HEADER_BD (LOFTMAG1, 40);
      HEADER_BD (LOFTMAG2, 40);
      HEADER_BS (LOFTPARAM, 70);
      HEADER_RC (LOFTNORMALS, 280);
      HEADER_BD (LATITUDE, 40);
      HEADER_BD (LONGITUDE, 40);
      HEADER_BD (NORTHDIRECTION, 40);
      HEADER_BL (TIMEZONE, 70);
      HEADER_RC (LIGHTGLYPHDISPLAY, 280);
      HEADER_RC (TILEMODELIGHTSYNCH, 280);
      HEADER_H (CMATERIAL, 347);
      HEADER_RC (SOLIDHIST, 280);
      HEADER_RC (SHOWHIST, 280);
      HEADER_RC (DWFFRAME, 280);
      HEADER_RC (DGNFRAME, 280);
      HEADER_B (REALWORLDSCALE, 290);
      HEADER_CMC (INTERFERECOLOR, 62);
      if (_obj->INTERFEREOBJVS->absolute_ref) {
        HEADER_H (INTERFEREOBJVS, 345);
      }
      if (_obj->INTERFEREVPVS->absolute_ref) {
        HEADER_H (INTERFEREVPVS, 346);
      }
      if (_obj->DRAGVS->absolute_ref) {
        HEADER_H (DRAGVS, 349);
      }
      HEADER_RC (CSHADOW, 280);
      HEADER_BD (SHADOWPLANELOCATION, 40);
    }

  ENDSEC();
